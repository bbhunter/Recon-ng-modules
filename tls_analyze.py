from sslyze.concurrent_scanner import ConcurrentScanner, PluginRaisedExceptionScanResult
from sslyze.plugins.compression_plugin import (
    CompressionScanCommand,
    CompressionScanResult,
)
from sslyze.plugins.fallback_scsv_plugin import (
    FallbackScsvScanCommand,
    FallbackScsvScanResult,
)
from sslyze.plugins.heartbleed_plugin import HeartbleedScanCommand, HeartbleedScanResult
from sslyze.plugins.openssl_ccs_injection_plugin import (
    OpenSslCcsInjectionScanCommand,
    OpenSslCcsInjectionScanResult,
)
from sslyze.plugins.robot_plugin import (
    RobotScanCommand,
    RobotScanResult,
    RobotScanResultEnum,
)
from sslyze.plugins.session_renegotiation_plugin import (
    SessionRenegotiationScanCommand,
    SessionRenegotiationScanResult,
)
from sslyze.plugins.session_resumption_plugin import SessionResumptionSupportScanCommand
from sslyze.server_connectivity_info import ServerConnectivityInfo
from sslyze.server_connectivity_tester import ServerConnectivityError
from sslyze.ssl_settings import TlsWrappedProtocolEnum

from recon.core.module import BaseModule


class Module(BaseModule):

    STARTTLS_PROTOCOL_DICT = {
        443: TlsWrappedProtocolEnum.HTTPS,
        587: TlsWrappedProtocolEnum.STARTTLS_SMTP,
        25: TlsWrappedProtocolEnum.STARTTLS_SMTP,
        5222: TlsWrappedProtocolEnum.STARTTLS_XMPP,
        5269: TlsWrappedProtocolEnum.STARTTLS_XMPP_SERVER,
        109: TlsWrappedProtocolEnum.STARTTLS_POP3,
        110: TlsWrappedProtocolEnum.STARTTLS_POP3,
        143: TlsWrappedProtocolEnum.STARTTLS_IMAP,
        220: TlsWrappedProtocolEnum.STARTTLS_IMAP,
        21: TlsWrappedProtocolEnum.STARTTLS_FTP,
        3268: TlsWrappedProtocolEnum.STARTTLS_LDAP,
        389: TlsWrappedProtocolEnum.STARTTLS_LDAP,
        3389: TlsWrappedProtocolEnum.STARTTLS_RDP,
        5432: TlsWrappedProtocolEnum.STARTTLS_POSTGRES,
    }

    meta = {
        "name": "TLS Stack Analyzer",
        "author": "jose nazario @jnazario",
        "description": "Contacts hosts with common TLS services (HTTPS, IMAPS, etc) open and evaluates the TLS configuration for flaws and known vulnerabilities. Updates the 'vulnerabilities' table.",
        "query": "SELECT DISTINCT host, port, ip_address FROM ports WHERE port in {} AND host NOT NULL AND ip_address NOT NULL".format(
            str(tuple(sorted(STARTTLS_PROTOCOL_DICT.keys())))
        ),
        "version": "1.1",
    }

    def module_run(self, hostportsip):
        for host, port, ip_address in hostportsip:
            self.heading("{0}:{1} ({2})".format(host, port, ip_address), level=0)
            port = int(port)
            try:
                tls_wrapped_protocol = self.STARTTLS_PROTOCOL_DICT[port]
            except KeyError:
                self.error("Protocol not found for port {}".format(port))
                continue
            try:
                server_info = ServerConnectivityInfo(
                    hostname=host,
                    port=port,
                    ip_address=ip_address,
                    tls_wrapped_protocol=tls_wrapped_protocol,
                )
                server_info.test_connectivity_to_server()
            except ServerConnectivityError as e:
                self.error("Could not connect to {0}:{1}: {2}".format(host, port, e))
                continue
            concurrent_scanner = ConcurrentScanner()
            concurrent_scanner.queue_scan_command(
                server_info, SessionRenegotiationScanCommand()
            )
            concurrent_scanner.queue_scan_command(server_info, CompressionScanCommand())
            concurrent_scanner.queue_scan_command(
                server_info, FallbackScsvScanCommand()
            )
            concurrent_scanner.queue_scan_command(server_info, HeartbleedScanCommand())
            concurrent_scanner.queue_scan_command(server_info, RobotScanCommand())
            concurrent_scanner.queue_scan_command(
                server_info, OpenSslCcsInjectionScanCommand()
            )
            concurrent_scanner.queue_scan_command(
                server_info, SessionResumptionSupportScanCommand()
            )
            for scan_result in concurrent_scanner.get_results():
                data = None
                if isinstance(scan_result, HeartbleedScanResult):
                    if scan_result.is_vulnerable_to_heartbleed:
                        data = {
                            "reference": "VULNERABLE - HEARTBLEED - Server is vulnerable to Heartbleed",
                            "example": "\n".join(scan_result.as_text()),
                        }
                elif isinstance(scan_result, RobotScanResult):
                    if (
                        scan_result.robot_result_enum
                        == RobotScanResultEnum.VULNERABLE_STRONG_ORACLE
                    ):
                        data = {
                            "reference": "VULNERABLE - ROBOT - Strong oracle, a real attack is possible",
                            "example": "\n".join(scan_result.as_text()),
                        }
                    elif (
                        scan_result.robot_result_enum
                        == RobotScanResultEnum.VULNERABLE_WEAK_ORACLE
                    ):
                        data = {
                            "reference": "VULNERABLE - ROBOT - Weak oracle, the attack would take too long",
                            "example": "\n".join(scan_result.as_text()),
                        }
                elif isinstance(scan_result, CompressionScanResult):
                    if scan_result.compression_name:
                        data = {
                            "reference": "VULNERABLE - Server supports Deflate compression",
                            "example": "\n".join(scan_result.as_text()),
                        }
                elif isinstance(scan_result, FallbackScsvScanResult):
                    if scan_result.supports_fallback_scsv:
                        data = {
                            "reference": "VULNERABLE - Signaling cipher suite not supported",
                            "example": "\n".join(scan_result.as_text()),
                        }
                        data = None
                elif isinstance(scan_result, OpenSslCcsInjectionScanResult):
                    if scan_result.is_vulnerable_to_ccs_injection:
                        data = {
                            "reference": "VULNERABLE - Server is vulnerable to OpenSSL CCS injection",
                            "example": "\n".join(scan_result.as_text()),
                        }
                elif isinstance(scan_result, SessionRenegotiationScanResult):
                    if scan_result.accepts_client_renegotiation:
                        data = {
                            "reference": "VULNERABLE - Server honors client-initiated renegotiations",
                            "example": "\n".join(scan_result.as_text()),
                        }
                elif isinstance(scan_result, PluginRaisedExceptionScanResult):
                    self.error("Scan command failed: {}".format(scan_result.as_text()))
                    continue
                if data:
                    data["host"] = host
                    data["category"] = "TLS vulnerability"
                    for key in sorted(data.keys()):
                        self.output("%s: %s" % (key.title(), data[key]))
                    self.insert_vulnerabilities(**data)
                    self.output(self.ruler * 50)

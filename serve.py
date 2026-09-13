#!/usr/bin/env python3
import os
import argparse
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler


class IndexHandler(SimpleHTTPRequestHandler):
    spa = False  # wird in main() gesetzt

    def list_directory(self, path):
        try:
            return super().list_directory(path)
        except OSError:
            self.send_error(404, "Nicht gefunden")
            return None

    def do_GET(self):
        if self.spa:
            # SPA-Fallback: nicht existierende Pfade → index.html
            path = self.translate_path(self.path)
            if not os.path.exists(path):
                self.path = "/index.html"
        return super().do_GET()

    def do_HEAD(self):
        if self.spa:
            path = self.translate_path(self.path)
            if not os.path.exists(path):
                self.path = "/index.html"
        return super().do_HEAD()


def _who_listens_on(port: int) -> str:
    """
    Versucht herauszufinden, was auf dem Port LISTEN macht.
    Primär: ss; Fallback: lsof.
    """
    # 1) ss (meist verfügbar auf aktuellen Linux-Systemen)
    try:
        # -ltn: listening tcp, numeric
        # -p: process info (benötigt ggf. Root)
        res = subprocess.run(
            ["ss", "-ltnp"],
            capture_output=True,
            text=True,
            check=False,
        )
        out = res.stdout.strip() or res.stderr.strip()

        # Einfacher Filter nach :<port> (Local Address enthält das meistens)
        needle = f":{port} "
        lines = [ln for ln in out.splitlines() if needle in ln]
        if lines:
            return "\n".join(lines)
        return out or "(keine Ausgabe von ss)"
    except FileNotFoundError:
        pass

    # 2) lsof (Fallback)
    try:
        res = subprocess.run(
            ["lsof", "-nP", "-sTCP:LISTEN", f"-iTCP:{port}"],
            capture_output=True,
            text=True,
            check=False,
        )
        out = (res.stdout.strip() or res.stderr.strip()).strip()
        return out or "(keine Ausgabe von lsof)"
    except FileNotFoundError:
        return "Weder 'ss' noch 'lsof' gefunden."


def main():
    parser = argparse.ArgumentParser(
        description="Einfacher HTTP-Server mit optionalem SPA-Fallback"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Bind-Adresse (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--dir", default=".", help="Root-Verzeichnis (default: .)")
    parser.add_argument(
        "--spa",
        action="store_true",
        help="SPA-Modus: bei 404 index.html ausliefern (für Client-Side-Routing)",
    )
    args = parser.parse_args()

    IndexHandler.spa = args.spa
    os.chdir(args.dir)

    print(f"Starte Server: http://{args.host}:{args.port}/")
    print(f"Root-Verzeichnis: {os.path.abspath(args.dir)}")
    if args.spa:
        print("SPA-Modus aktiv: 404 → /index.html")

    try:
        server = HTTPServer((args.host, args.port), IndexHandler)
    except OSError as e:
        if getattr(e, "errno", None) == 98:
            details = _who_listens_on(args.port)
            raise RuntimeError(
                f"Port {args.host}:{args.port} ist bereits belegt (EADDRINUSE / Errno 98).\n"
                f"Was lauscht dort?\n{details}"
            ) from e
        raise

    server.serve_forever()


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(str(e))
        raise SystemExit(1)

import argparse
import logging
import os

from mcp_obsidian.obsidian import Obsidian


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Test the Obsidian.find_file_by_name helper."
    )
    parser.add_argument(
        "filename",
        help="Name of the file to resolve (e.g., 'Daily Note.md' or 'Daily Note').",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("OBSIDIAN_HOST", "127.0.0.1"),
        help="Obsidian API host (defaults to OBSIDIAN_HOST env var or 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("OBSIDIAN_PORT", "27124")),
        help="Obsidian API port (defaults to OBSIDIAN_PORT env var or 27124).",
    )
    parser.add_argument(
        "--protocol",
        default=os.getenv("OBSIDIAN_PROTOCOL", "https"),
        choices=["http", "https"],
        help="Protocol for the Obsidian API (defaults to OBSIDIAN_PROTOCOL env var).",
    )
    parser.add_argument(
        "--verify-ssl",
        action="store_true",
        help="Enable SSL verification when using https.",
    )
    parser.add_argument(
        "--log-level",
        default="DEBUG",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Logging verbosity (default: DEBUG).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, "DEBUG"))
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("mcp_obsidian").setLevel(logging.DEBUG)

    api_key = os.getenv("OBSIDIAN_API_KEY")
    if not api_key:
        parser.error(
            "OBSIDIAN_API_KEY environment variable must be set to run this script."
        )

    client = Obsidian(
        api_key=api_key,
        protocol=args.protocol,
        host=args.host,
        port=args.port,
        verify_ssl=args.verify_ssl,
    )

    resolved_path = client.find_file_by_name(args.filename)
    print(f"Matched path: {resolved_path}")


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Main entry point for the extensible hash index simulator
Ejecuta el simulador de índice hash extensible
"""

from cli import ExtensibleHashCLI


def main():
    """Función principal que inicia la aplicación"""
    cli = ExtensibleHashCLI()
    cli.run()


if __name__ == "__main__":
    main()

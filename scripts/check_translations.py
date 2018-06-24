# -*- coding: utf-8 -*-
"""
Future place for validating the translations.
"""

def main():
    status = True
    # TODO: Validate here.
    return status

if __name__ == '__main__':
    status = main()
    if(not status):
        raise RuntimeError("Failed translation checks")
    else:
        print("Success")

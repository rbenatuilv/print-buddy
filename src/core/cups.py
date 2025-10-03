import cups


class CUPSManager:
    def __init__(self):
        try: 
            self.conn = cups.Connection()
        except:
            print("FAILED TO CONNECT TO CUPS")
            self.conn = None

        self.CUPS_STATE_MAP = {
            3: "idle",
            4: "printing",
            5: "stopped"
        }

    def get_printers(self) -> list[dict]:
        """
        Returns CUPS printers info on a list of dictionaries
        """
        if self.conn is None:
            return []

        printers = self.conn.getPrinters()
        result = []
        for name, attrs in printers.items():
            result.append({
                "name": name,
                "location": attrs.get("printer-location"),
                "status": self.CUPS_STATE_MAP.get(attrs.get("printer-state"), "unknown"),
            })
        
        return result

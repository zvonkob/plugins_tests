from lxml import etree


def main():

    # 1. Naložimo XSD shemo
    with open("shema.xsd", "rb") as f:
        schema_root = etree.XML(f.read())

    schema = etree.XMLSchema(schema_root)

    # 2. Naložimo XML dokument
    xml_doc = etree.parse("podatki.xml")

    # 3. Izvedemo validacijo
    if schema.validate(xml_doc):
        print("XML dokument je veljaven.")
    else:
        print("XML dokument NI veljaven.")

        # Izpišemo napake validacije
        for error in schema.error_log:
            print(f"Linija {error.line}: {error.message}")


if __name__ == "__main__":
    main()

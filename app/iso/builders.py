
from lxml import etree
from datetime import datetime, timezone

NS = {
  "pacs": "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10",
  "pain": "urn:iso:std:iso:20022:tech:xsd:pain.001.001.11",
  "camt": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.12"
}

def pacs008(data: dict) -> bytes:
    doc = etree.Element("Document", nsmap={None: NS["pacs"]})
    root = etree.SubElement(doc, "FIToFICstmrCdtTrf")
    grp = etree.SubElement(root, "GrpHdr")
    etree.SubElement(grp, "MsgId").text = data.get("msg_id","zkorigo")
    etree.SubElement(grp, "CreDtTm").text = datetime.now(timezone.utc).isoformat()
    etree.SubElement(grp, "NbOfTxs").text = "1"

    txi = etree.SubElement(root, "CdtTrfTxInf")
    pmt = etree.SubElement(txi, "PmtId")
    etree.SubElement(pmt, "EndToEndId").text = data.get("end_to_end_id","N/A")

    rmt = etree.SubElement(txi, "RmtInf")
    etree.SubElement(rmt, "Ustrd").text = data.get("unstructured","On-chain reference")

    # Optional: supplementary
    spl = etree.SubElement(txi, "SplmtryData")
    env = etree.SubElement(spl, "Envlp")
    add = etree.SubElement(env, "AddtlData")
    for k,v in (data.get("supplementary") or {}).items():
        elem = etree.SubElement(add, k)
        elem.text = str(v)

    return etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def pain001(data: dict) -> bytes:
    doc = etree.Element("Document", nsmap={None: NS["pain"]})
    cst = etree.SubElement(doc, "CstmrCdtTrfInitn")
    grp = etree.SubElement(cst, "GrpHdr")
    etree.SubElement(grp, "MsgId").text = data.get("msg_id","zkorigo")
    etree.SubElement(grp, "CreDtTm").text = datetime.now(timezone.utc).isoformat()
    pmt = etree.SubElement(cst, "PmtInf")
    etree.SubElement(pmt, "PmtInfId").text = data.get("payment_info_id","PMT-1")
    etree.SubElement(pmt, "NbOfTxs").text = "1"
    return etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def camt053(data: dict) -> bytes:
    doc = etree.Element("Document", nsmap={None: NS["camt"]})
    stmt = etree.SubElement(doc, "BkToCstmrStmt")
    grp = etree.SubElement(stmt, "GrpHdr")
    etree.SubElement(grp, "MsgId").text = data.get("msg_id","zkorigo")
    return etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding="UTF-8")

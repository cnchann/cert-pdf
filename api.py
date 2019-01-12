import json
import base64

import issuer_helpers
import verify_helpers

pdf_import_path = 'PDFs'
json_export_path = 'configuration/blockcert_certificates'
summary_export_path = 'summary.json'
tools_conf = 'configuration/cert_tools_conf.ini'
issuer_conf = 'configuration/cert_issuer_conf.ini'
pubkey_list = ['mubib9QNSNfBZkphQb3cCXG6giGKzA9k3X']

# FUNCTION issue_batch - Load a set of PDF files and finally deploy them on the blockchain
#
# import_path - the directory where all PDFs are stored which need to be issued
# export_path - the destination of the issued certs (json files)
# summary_path - the destination of the summary json file, which records the information of issued certs
# name_pattern - the format of filename. |NAME|, |DOCID| are wildcards to match the corresponding info
#               PLAESE DON'T include '.pdf' in namePattern

def issue_batch(import_path, export_path, summary_path, name_pattern = '|DOCID|-|NAME|'):

    print('\n[INFO] Creating roster file ...')
    list_DOCID = issuer_helpers.create_roster(import_path, name_pattern)
    print('\n[INFO] Clearing the working directories ...')
    issuer_helpers.clear()
    print('\n[INFO] Creating certificate templates ...')
    issuer_helpers.create_template()
    print('\n[INFO] Instantiating certificates ...')
    issuer_helpers.create_certificates()
    print('\n[INFO] Issuing certificates ...')
    issuer_helpers.modify_ini(issuer_conf, 'ISSUERCONF', 'blockchain_certificates_dir', export_path)
    issuer_helpers.issue_certificates(export_path)
    print('\n[INFO] Generating summary file ...')
    issuer_helpers.generate_summary(export_path, summary_export_path, list_DOCID)
    print('\n[INFO] All steps finished.\n')

# FUNCTION verify_cert - Verify whether a cert
#                        1) is generated by specified issuer
#                        2) is confirmed on the blochchain / revoked / tampered
#
# pubkey_list - the official public keys of the issuer
# NOTE: only testnet and mainnet of bitcoin are supported

def verify_cert(cert_path, pubkey_list):
    
    result = []

    ret = verify_helpers.check_confirmation_and_issuer(cert_path, pubkey_list)
    ret2 = verify_helpers.cert_verify(cert_path)
    ret.update(ret2)

    prev = True
    for x in ret.keys():
        result.append({'name' : x, 'passed' : prev and ret[x]})
        if prev and ret[x]:
            msg = 'passed'
        elif prev and not ret[x]:
            msg = 'not passed'
        else:
            msg = 'skipped'
        print('%27s' % x + ' - ' + msg)
        prev = prev and ret[x]

    result.append({'name' : '*OVERALL VALIDATION', 'passed' : not False in ret.values()})
    print('%27s' % '*OVERALL VALIDATION' + ' - ' + ('PASSED' if not False in ret.values() else 'NOT PASSED'))

    return result

# FUNCTION extract_pdf - Extract the PDF file inside the cert json file

def extract_pdf(cert_path, export_path):
    try:
        with open(cert_path) as f:
            output = open(export_path, 'wb')
            data = json.load(f)
            output.write(base64.decodestring(data['PDFinfo'].encode('utf-8')))
            print('[INFO] Extract succeeded!')
    except Exception as e:
        print(e)


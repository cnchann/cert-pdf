# PDF_Embedded_Blockcert
This is a variant of Blockcert which enables users to embed PDF files inside blockcerts and deploy them on the blockchain.

## Install

1. Please make sure that you have the recommanded [python environment](https://github.com/blockchain-certificates/cert-issuer/blob/master/docs/virtualenv.md) provided to run the blockcert project.

2. Install the **modified** blockcert module via following commands:

```
git clone https://github.com/ppfish45/cert-tools.git && cd cert-tools && sudo pip install . && cd ../
git clone https://github.com/ppfish45/cert-issuer.git && cd cert-issuer && sudo pip install . && cd ../
git clone https://github.com/ppfish45/cert-verifier.git && cd cert-verifier && sudo pip install . && cd ../
```

3. Clone cert-pdf and enter the directory

```
git clone https://github.com/ppfish45/cert-pdf.git && cd cert_pdf
```

## Usage

### Issue a batch of PDF files

1. Configure the issuer & blockchain account info in `configuration/cert_issuer_conf.ini` and `configuration/cert_tools_conf.ini`. Please do not modify the the directory related to `template`, `unsigned_certificates` and `roster`.

2. Import `cert_pdf/api.py` and run following code in python
  ``` 
  issue_batch(import_path, export_path, summary_path, name_pattern = '|DOCID|-|NAME|')
  ```

3. For details of parameters, please refer to `cert_pdf/api.py`

4. **NOTICE THAT THE BITCOIN TESTNET ACCOUNT USED IS ONLY FOR TEST. PLEASE MODIFY IT TO YOUR OWN'S.**

### Verify an Certificate

1. Import `cert_pdf/api.py` and run following code in python
  ``` 
  verify_cert(cert_path, pubkey_list)
  ```

2. Note that pubkey_list is list of valid public keys of the issuer.

3. This function will check 6 items of the cert.
```
   transaction is confirmed - passed
  issued by specific issuer - passed
 has not been tampered with - passed
            has not expired - passed
       has not been revoked - passed
        issuer authenticity - passed
```

### Extract the PDF File inside an Certificate

1. Import `cert_pdf/api.py` and run following code in python
  ``` 
  extract_pdf(cert_path, export_path)
  ```
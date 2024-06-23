# coding=utf-8
__author__ = 'pan'

import hashlib
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class AlgorithmUtil(object):
    def __init__(self, app_key):
        self.app_key = app_key

    def build_rsa_sign(self, params, private_key):
        clean_params = AlgorithmUtil._clean_empty_pair(params)
        link_string = AlgorithmUtil._create_link_string(clean_params)
        link_string = link_string + "&appKey=" + self.app_key
        sign = RsaAlgorithmUtil.gen_sign(link_string, private_key)
        return sign

    def verify_rsa_sign(self, params, public_key):
        if 'sign' not in params:
            return False
        sign = params['sign']
        clean_params = AlgorithmUtil._clean_empty_pair(params)
        content = AlgorithmUtil._create_link_string(clean_params)
        content = content + "&appKey=" + self.app_key
        return RsaAlgorithmUtil.verify_sign(content, sign, public_key)

    @staticmethod
    def _create_link_string(params):
        keys = params.keys()
        keys.sort()
        terms = list()
        for key in keys:
            value = params[key]
            terms.append(key + '=' + str(value))
        return '&'.join(terms)

    @staticmethod
    def _clean_empty_pair(params):
        result = dict()
        for key in params:
            value = params[key]
            if key.lower() == 'sign' or key.lower == 'appkey':
                continue
            result[key] = value
        return result

    @staticmethod
    def md5_sum(data):
        md = hashlib.md5()
        md.update(data)
        return md.hexdigest()[8:-8]


class RsaAlgorithmUtil(object):
    @staticmethod
    def gen_sign(content, decode_private_key):
        private_key = RsaAlgorithmUtil.decode_private_key(decode_private_key)
        return RsaAlgorithmUtil.compute_sign(content, private_key)

    @staticmethod
    def verify_sign(content, sign, decode_public_key):
        public_key = RsaAlgorithmUtil.decode_public_key(decode_public_key)
        signer = PKCS1_v1_5.new(public_key)
        digest = SHA256.new(content)
        # Assumes the data is base64 encoded to begin with
        if signer.verify(digest, base64.b64decode(sign)):
            return True
        return False

    @staticmethod
    def compute_sign(content, key):
        h = SHA256.new(content)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(h)
        return base64.b64encode(signature)

    @staticmethod
    def separate_key(base64_key):
        terms = list()
        start = 0
        length = 64
        total_length = len(base64_key)
        count = total_length / length + 1
        for i in range(0, count):
            if start + length < total_length:
                term = base64_key[start:start + length]
            else:
                term = base64_key[start:]
            terms.append(term)
            start += length
        res = "\n".join(terms)
        return res

    @staticmethod
    def decode_private_key(base64_key):
        res = RsaAlgorithmUtil.separate_key(base64_key)
        key = "-----BEGIN RSA PRIVATE KEY-----\n" + res + "\n-----END RSA PRIVATE KEY-----"
        return RSA.importKey(key)

    @staticmethod
    def decode_public_key(base64_key):
        res = RsaAlgorithmUtil.separate_key(base64_key)
        key = "-----BEGIN PUBLIC KEY-----\n" + res + "\n-----END PUBLIC KEY-----"
        return RSA.importKey(key)

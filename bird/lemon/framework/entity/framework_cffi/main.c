#include "cdef.h"
#include <stdio.h>
int main()
{
    //公钥
    char *pkey_str = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2kcrRvxURhFijDoPpqZ/IgPlA\ngppkKrek6wSrua1zBiGTwHI2f+YCa5vC1JEiIi9uw4srS0OSCB6kY3bP2DGJagBo\nEgj/rYAGjtYJxJrEiTxVs5/GfPuQBYmU0XAtPXFzciZy446VPJLHMPnmTALmIOR5\nDddd1Zklod9IQBMjjwIDAQAB\n-----END PUBLIC KEY-----";
    //用私钥加密过的字符串
    char *pri_str = "YFSGlJTpNYakrZuZqZ55dcA5mVUb/JQBr3hdDjODsAVSdoVVytIagk9Wt0CD/uX+7jGL9pqev8/u0I0ZBKEmz5huXp8TdZSnskCZ7GTeHNW0VPJcW8OcBxAValA0jQSv2mBP+tc1r6mdvf66GEzhvgBfTnp3Sp7V3dijJ9bNstIDyrGm/BlByhcMr3UqXjTFJaui6t5TxvZhCuSV9sg+xVVA+sR3uFI78b5lKomg5Vu31EBZvXASlFfaOc4StltRUH2aSiRqjnbXe8dlRZO0Ih44htYs2QfehzeQnPHtTwNHUvtVIVcIdI/7j9yfy5es13QeIgfKghY/ENUnB2V7iA==";
    char decrypted_buf[10240];
    rsa_decrypt(pri_str, pkey_str, 1, decrypted_buf);
    printf("%s\n", decrypted_buf);
    return 0;
}

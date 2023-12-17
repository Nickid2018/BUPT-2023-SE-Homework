import base64

import rsa

public_key = rsa.PublicKey.load_pkcs1_openssl_pem(b'-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtHG1pFyFM70d7TmCLx90p1XkzAPTFeVXkmVmfFW5UauCf2rSdBf4Z7j34HdQzkaaS6y8qgdWhvEHExlNr35BY2d+F3rITKO3elyl1VsWAjK8gGFo8hLeTMGLnBq5dEhYZvbaSPF8SE07EyMJnUnBU1ICqsQ7+QdkBx/1XxM8k27UAQIbpOls5oHb3brOcbFGbPAdQU8ANUIq384AVVd6tdw99+OEiWwJTKoqewViWO6TgqYmCm0cC3Dydd2L+DQWwWcH49630Yw43Seyw55nqqIJeeE0wycX2xUT8x11ty0HvsMEpURxmImLMVBUBtaZqi9mJkARguAlqweMaV/r4TgGAv67ntKAjfppNL5i3IUDPafNIGVhB0aeucXD5rJYkG38ZluWX/5a5yZM4Kl0e1b8N9lRG4wo4ric+vCXDJO/osGGFwjRN7r3zZVDXWQMlv1cStgUa5BcJNPH4ENa5/WOF7bMfLMwgM/2o9ayBe5i7CcKq6fkqte0vF93f8NyPhE3eFWlRGyvdWg+AUruWJJurFQ/Ue6SkxjdKkKsk77jwFNxAin6E0IM1JASqAWgRGXfmSDPg9fjod9ae4rmoO1jV5FwyVBcTLy+qkdKw8VrXo8SSm8M1YD1x4TSsQKzdoHz1F+IvJikPD7slBIwJYRjvtMW0yK+KaC6MkB4UTECAwEAAQ==\n-----END PUBLIC KEY-----')
private_key = rsa.PrivateKey.load_pkcs1(b'-----BEGIN RSA PRIVATE KEY-----\n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\n-----END RSA PRIVATE KEY-----')


def sign(sign_text):
    return rsa.sign(sign_text.encode(), private_key, 'SHA-256')


def verify_signature(verify_str, signature):
    return rsa.verify(verify_str.encode(), signature, public_key)


str = sign("hello")
print(str)
print(verify_signature("hello", str))
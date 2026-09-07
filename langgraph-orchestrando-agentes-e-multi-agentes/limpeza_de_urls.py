from urllib.parse import urlparse, urlunparse

url = "https://www.exemplo.com/restaurantes?pagina=2&ordenar=popularidade"
parsed_url = urlparse(url)
print(parsed_url)  # Saída: ParseResult(scheme='https', netloc='www.exemplo.com', path='/restaurantes', params='', query='pagina=2&ordenar=popularidade', fragment='')

clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
print(clean_url)  # Saída: https://www.exemplo.com/restaurantes
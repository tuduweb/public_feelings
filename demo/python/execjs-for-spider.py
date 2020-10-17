import execjs
import re

resp_body = "<script>document.cookie=('_')+('_')+('j')+('s')+('l')+('_')+('c')+('l')+('e')+('a')+('r')+('a')+('n')+('c')+('e')+('_')+('s')+('=')+((+true)+'')+([2]*(3)+'')+(~~[]+'')+(0+1+0+1+'')+(4+5+'')+(-~1+'')+(5+'')+((2)*[4]+'')+(-~(8)+'')+(1+[0]-(1)+'')+('.')+(2+'')+(5+'')+((2<<1)+'')+('|')+('-')+(-~false+'')+('|')+('r')+(1+4+'')+('b')+('m')+('B')+('e')+('H')+('f')+('Y')+('I')+('x')+('k')+('R')+('G')+('r')+(1+2+'')+('T')+(4+4+'')+('h')+('h')+('y')+('W')+('W')+('v')+('W')+('%')+(0+1+0+1+'')+('F')+('s')+('%')+(1+2+'')+('D')+(';')+('m')+('a')+('x')+('-')+('a')+('g')+('e')+('=')+((1+[2]>>2)+'')+(3+3+'')+(~~[]+'')+(~~''+'')+(';')+('p')+('a')+('t')+('h')+('=')+('/');location.href=location.pathname+location.search</script>"
print(resp_body)

get_js = re.findall(r'<script>(.*?)</script>', resp_body)[0]
get_js = re.sub('document.cookie=','return(', get_js)
get_js = re.sub(';location.href',');location.href', get_js)
get_js = "function getClearance(){" + get_js + "};"
content = execjs.compile(get_js)
temp = content.call('getClearance')
clearance = temp.split(";")[0]
print(clearance)
# M3CircleListParser  
M3( http://www.m3net.jp/ )公式からサークルリストをcsvで吐き出すだけの簡単なPythonスクリプトです。  

## つかいかた  
python M3CircleListParser.py \<output csv filename\>  

## 注意事項  
* Python3未対応 (HTMLParser->html.parser, urllib2->urilib.requestにimport修正すれば動くはず)
* M3サークルリストのurl(m3_url)は対象のイベントごとに適当に変更してください。

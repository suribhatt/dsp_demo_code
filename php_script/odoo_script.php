<?php
class OdooApi
{
    protected $_cookieFileLocation = './Odoocookie.txt';
    protected $_header     = array(
        'Content-Type: application/json'
      );
    protected $cr; // curl cursor
    protected $url;
 
	public function __destruct() {
            curl_close($this->cr);
        }

    public function __construct(){
            $this->_cookieFileLocation = dirname(__FILE__).'/Odoocookie.txt';
            $this->cr = curl_init();
            $this->url = "http://localhost:8069";
    }

    public function callOdooUrl($url = null, $method=null, $params=null){
        if (!$url) {
            throw new Exception('You should set an URL to call.');
        }
        if(!$method)
            throw new Exception('You should set a method to call.');
        curl_setopt($this->cr,CURLOPT_URL,$this->url.$url);
        curl_setopt($this->cr,CURLOPT_RETURNTRANSFER,true);
        curl_setopt($this->cr,CURLOPT_ENCODING, ''); 
        curl_setopt($this->cr,CURLOPT_MAXREDIRS, 30);
        curl_setopt($this->cr,CURLOPT_MAXREDIRS, 0);
        curl_setopt($this->cr,CURLOPT_COOKIEFILE, $this->_cookieFileLocation);
        curl_setopt($this->cr,CURLOPT_COOKIEJAR, $this->_cookieFileLocation);
        curl_setopt($this->cr, CURLOPT_FOLLOWLOCATION, true);                                                                     
        curl_setopt($this->cr, CURLOPT_POSTFIELDS, $params);                                                                  
        curl_setopt($this->cr, CURLOPT_HTTP_VERSION, true); 
        curl_setopt($this->cr,CURLOPT_FAILONERROR,true);
        curl_setopt($this->cr,CURLOPT_HTTPHEADER,$this->_header);
        curl_setopt($this->cr,CURLOPT_CUSTOMREQUEST,$method);
        $data = curl_exec($this->cr);
        $status = curl_getinfo($this->cr,CURLINFO_HTTP_CODE);
        if(curl_errno($this->cr)){
            $msg = curl_error($this->cr);
            return[
                'status'=>0,
                'message'=>$msg
            ];
        }
        else{
            return[
                'status'=>1,
                'data'=>json_decode($data)
            ];   
            }
        }
}

$odooApi = new OdooApi();

$params = json_encode(array("jsonrpc"=>"2.0",
"params"=> array("db"=>"demo", "login"=>"admin","password"=>"admin")));
$data = $odooApi->callOdooUrl("/web/session/authenticate", "POST", $params);

?>
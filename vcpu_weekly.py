import requests
import urllib3
import json
from pathlib import Path
from requests.auth import HTTPBasicAuth
import csv
from template import html_template
from loader_template import html_loader_template
import zipfile
import time

#author : RUSHABH JAIN 
def get_cluster_name(pc_creds):
     PC_IP = pc_creds[0]
     user=pc_creds[1]
     passw=pc_creds[2]
     mx_cpu_file = "downloaded_report_instance/Weekly_Max_CPU_Usage.csv/1_max_cpu_usage.csv"
     clusters=[]
     with open(mx_cpu_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                for i in range(len(row)):
                     row[i] = row[i].strip()
                clusters.append(row)
    # print(clusters)
     #for obj in clusters[1:]:
        #endpoint = f"https://{PC_IP}:9440/api/nutanix/v3/clusters/{obj[0]}"
        #headers = {"Content-Type": "application/json", "charset": "utf-8"}
        #response = requests.get(endpoint,auth=(user, passw),headers=headers,verify=False)
        
        #name = response.json()["status"]["name"]
        #obj.append(name)
     #print(clusters)
     return clusters
     
                
def get_report(pc_creds):
        
        PC_IP = pc_creds[0]
        user=pc_creds[1]
        passw=pc_creds[2]
        endpoint=f"https://{PC_IP}:9440/api/nutanix/v3/report_configs/list"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        request_headers = {"Content-Type": "application/json", "charset": "utf-8"}
        
        request_body = {"kind": "report_config", "length": 500}
        result = requests.post(endpoint,data=json.dumps(request_body), headers=request_headers,auth=(user, passw), verify=False)
        
        if result.status_code!=200:
             print("ERROR IN POST REQUEST FOR CONFIG GET_REPORT FUNCTION!")
             return None
        rc_uuid=""
      
        #GETTING THE REPORT CONFIG UUID
        for obj in result.json()["entities"]:
            if(obj["spec"]["name"]=="Weekly_Max_CPU_Usage"):
                rc_uuid = obj["metadata"]["uuid"]
                break
        print("     ->Report config uuid:",rc_uuid)

        instances=[]
        endpoint=f"https://{PC_IP}:9440/api/nutanix/v3/report_instances/list"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        request_body = {"kind": "report_instance", "length": 500}
        result = requests.post(endpoint, data=json.dumps(request_body),headers=request_headers,auth=(user, passw), verify=False)
        if result.status_code!=200:
             print("ERROR IN POST REQUEST FOR INSTANCE GET_REPORT FUNCTION!")
             return None
       
        #GETTING THE INSTANCE UUID
        for obj in result.json()["entities"]:
            if(obj["spec"]["resources"]["report_config_reference"]["uuid"]==rc_uuid):
                instances.append(obj)

        sorted_instances = sorted(instances,reverse=True, key=lambda x: x["metadata"]["creation_time"])
        #print(sorted_instances)

        #print(instances)
        #SORTING THE INSTANCES TO GET THE LATEST INSTANCE
        inst = sorted_instances[0]["metadata"]["uuid"]
        print("     ->Instance uuid:",inst)


        #DOWNLOADING THE INSTANCE
        endpoint = f"https://{PC_IP}:9440/api/nutanix/v3/reports/download/report_instance_csv/{inst}"
        headers = {"Content-Type": "application/zip", "charset": "utf-8"}
        response = requests.get(endpoint,auth=(user, passw),headers=headers,verify=False)
        if result.status_code!=200:
             print("ERROR IN GET REQUEST FOR DOWNLOADING FILES IN  GET_REPORT FUNCTION!")
             return None
        file_inst = "downloaded_report_instance.zip"
        
        with open(file_inst, 'wb') as file:
            file.write(response.content)
            print(f"     ->Report Instance {inst} was downloaded successfully!")
        
        #extracting the downloaded files
        with zipfile.ZipFile("downloaded_report_instance.zip", 'r') as zip_ref:
            zip_ref.extractall("downloaded_report_instance")

        #print("Downloaded files are extracted in downloaded_report_instance folder!")
        return 1
def main():
    output_file = "templates/output.html"
    lt = html_loader_template
    with open(output_file, 'w') as file:
            file.write(lt)
    pc_creds=[]
    print("\n \n \n")

    with open("data.json",'r') as file:
         data = json.load(file)

    #print(data)
    pc_creds = [x for x in data.values()]
    print(pc_creds)
    #return
         
    #with open("data.csv", 'r') as file:
     #       csv_reader = csv.reader(file)
      #      for row in csv_reader:
      #          pc_creds = row
    final_data=[]
    res = get_report(pc_creds)
    if res==None:
         return
    
    max_cpu_usage_file = "downloaded_report_instance/Weekly_Max_CPU_Usage.csv/1_max_cpu_usage.csv"
    vms_vcpu_file = "downloaded_report_instance/Weekly_Max_CPU_Usage.csv/2_VMS_VCPU_DATA.csv"
    clusters = get_cluster_name(pc_creds)
   # print(clusters)

    cluster_name_list = []
    for data in clusters[1:]:
         obj={}
         obj["uuid"] = data[-1]
         obj["max_cpu_usage"] = data[-2]
         obj["phy_cores"] = data[3]
         obj["num_hosts"] = data[1]
         obj["name"] = data[0]
         obj["num_vms"] = 0
         obj["num_vcpus"] = 0
         final_data.append(obj)
         cluster_name_list.append(obj["name"])
    #print(final_data)

    vcpu_vms = []
    with open(vms_vcpu_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                for i in range(len(row)):
                     row[i] = row[i].strip()
                vcpu_vms.append(row)
   
    for obj in final_data:
         curr_vcpu=0
         vm_count = 0
         for item in vcpu_vms[1:]:
              if str(obj["name"])==str(item[0]):
                
                   curr_vcpu=curr_vcpu + int(item[-1])
                   vm_count = vm_count + 1
              #else:
                   #print(obj["name"],type(obj["name"]))
                   #print(item[1],type(item[1]))
              
         obj["num_vcpus"] = curr_vcpu
         obj["num_vms"] = vm_count

   # print(final_data)
          
                    
    ht = html_template
    lt = html_loader_template
    html_boxes=""         
    for cluster_data in final_data:
        cluster_name = cluster_data["name"]
        number_of_hosts = cluster_data["num_hosts"]
        number_of_vms = cluster_data["num_vms"]
        number_of_phyc = int(cluster_data["phy_cores"])
        max_cpu_usage = float(cluster_data["max_cpu_usage"].rstrip("%").strip())
        pro_vcpus = cluster_data["num_vcpus"]
        defi_cpu_usage = 80-max_cpu_usage
        ideal = (defi_cpu_usage*pro_vcpus)/100 + (pro_vcpus)
        curr_vcpu_ratio = round(int(pro_vcpus)/int(number_of_phyc),3)
        additional_vcpus_possible = ideal-pro_vcpus
        new_vcpus_ratio = ideal/number_of_phyc


        html_box = f"""
        <tr>
        <td> {cluster_name}</td>
        <td> {number_of_hosts}</td>
         <td> {number_of_vms}</td>
        <td> {pro_vcpus}</td>
        <td> {number_of_phyc}</td>
        <td> {max_cpu_usage}</td>
        <td style="background-color:rgb(235, 224, 148)" > {curr_vcpu_ratio}</td>
        <td> {round(ideal,3)}</td>
        <td> {round(additional_vcpus_possible,3)}</td>
         <td style="background-color: rgb(179, 235, 233)"> {round(new_vcpus_ratio,3)}</td>
        </tr>
        """
    
        html_boxes += html_box
        
    pc_name = "Prism Central :" + pc_creds[0]
    #the final html code to display data
    try:
        
        final_html = ht.format(data=html_boxes,pc_name =pc_name)
        output_file = "templates/output.html"
        
          
        with open(output_file, 'w') as file:
            file.write(final_html)
    except Exception:
        print("Error writing data to final html !!!")
        return
    
    with open("generated_vcpu_result.json","w") as json_file:
         json.dump(final_data,json_file,indent=4)
        
    print("     ->Check generated_vcpus_result.json for the output!")


if __name__ == '__main__': 
    main()




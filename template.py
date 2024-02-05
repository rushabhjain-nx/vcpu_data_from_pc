html_template="""
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>vcpu_analysis</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

	</head>
    
	<body>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

        <div class="container-fluid " style="margin-top: 10px;border-radius: 2px;" >
            <nav class="navbar navbar-expand-lg navbar-light " style="background-color: #7855FA">
                <div class="container-fluid">
                    <img src="/static/ntnx.svg" width="150" height="40" alt="">
                   
                        <span  style="margin-right: 40%;color: white;" >
                            vCPU Ratio Analysis for {pc_name}
                          </span>
                    
                 
                </div>
               
            </nav>
          </div>
        <div class="container-fluid" style="margin-top: 10px;border-radius: 2px;">
        <table class="table table-bordered" style="border-radius: 5px;">
            <thead class="thead" style="border-radius: 5px;background-color:#131313;color: white"
            ;">
              <tr>
                <th scope="col">Cluster Name</th>
                <th scope="col">Number of Hosts</th>
                <th scope="col">Number of VMs</th>
                <th scope="col">Provisioned vCPUs (Powered ON+OFF)</th>
                <th scope="col">Number of Physical Cores</th>
                <th scope="col">Maximum CPU Usage for the week %</th>
                <th scope="col">Current vCPU Ratio</th>
                <th scope="col">Ideal vCPUs for cluster</th>
                <th scope="col">Additional vCPUs possible</th>
                <th scope="col">Future vCPU Ratio</th>
              
              </tr>
            </thead>
            <tbody>
              {data}
              
             
            </tbody>
          </table>
          
         
        </div>
	</body>
	
</html>

"""
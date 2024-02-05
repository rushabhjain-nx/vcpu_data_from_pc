html_loader_template="""
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>vcpu_analysis</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    
     <style>
      .loader {
  border: 16px solid #f3f3f3; /* Light grey */
  border-top: 16px solid #7855FA; /* Blue */
  border-radius: 50%;
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
  }

    @keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
  }
    </style>
	</head>
    
	<body>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

        <div class="container-fluid " style="margin-top: 10px;border-radius: 2px;" >
            <nav class="navbar navbar-expand-lg navbar-light " style="background-color: #7855FA">
                <div class="container-fluid">
                    <img src="ntnx.svg" width="150" height="40" alt="">
                   
                        <span  style="margin-right: 50%;color: white;" >
                            vCPU Ratio Analysis
                          </span>
                    
                 
                </div>
               
            </nav>
          </div>
        
          
          <div class="loader container-fluid" style="margin-top: 100px;">
          </div>
          <div class="container-fluid"  style="margin-top: 20px;">
          <center> Loading Data </center>
          </div>
          

	</body>
	
</html>

"""
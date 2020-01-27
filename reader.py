import csv
import random
from datetime import date

class Report:
    #Variable Declarations
    today = today = date.today().strftime("%b-%d")
    html_opening_tags = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>DAQ Oversight """+today+"""</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    </head>
    <style>
        h1{
            padding: 10px;
            font-size: 1.5em;
        }
        table{
            padding:10px;
        }
        td{
            padding:5px 20px;
        }
        .grayed{
            background-color: gray;
        }
    </style>
    <body>
    <div class="container-fluid">
        <h1 class="display-4">DAQ Oversight for """+today+""" <small class="h6 text-muted">click headings to sort columns</small></h1>
        
        <table class="table table-hover" id="table"> 
            <thead>
                <tr class="text-center">
                    <th scope="col">Name</th>
                    <th scope="col">Days</th>
                    <th scope="col">SR</th>
                    <th scope="col">Case</th>
                    <th scope="col">Status</th>
                    <th scope="col">Service</th>
                    <th scope="col">Feedback</th>
                    <th scope="col" class="align-middle"><img src="https://img.icons8.com/officel/16/000000/checkmark.png"></th>
                </tr>
            </thead>
            <tbody>    
    """
    html_closing_tags = """
            </tbody>
        </table>
    <div> 
    <script>
        var checkboxes = document.getElementsByTagName('input');
        for(var i = 0; i<checkboxes.length; i++){
            checkboxes[i].addEventListener('change', function(){
                this.parentElement.parentElement.classList.toggle('grayed');
            })
        }

        const myTable = document.querySelector('#table');
        // select all trs below the header:
        const trs = [...myTable.querySelectorAll('tr')].slice(1);

        myTable.addEventListener('click', ({ target }) => {
        if (!target.matches('th')) return;
        const thIndex = Array.prototype.indexOf.call(target.parentElement.children, target);
        const getText = tr => tr.children[thIndex].textContent;
        trs.sort((a, b) => getText(a).localeCompare(getText(b), undefined, { numeric: true }));
        trs.forEach(tr => myTable.appendChild(tr));
        });


    </script>
    </body>
    </html>"""

    #element names from salesforce report
    name, link, days_open, service_level, sr_number, status, opened_date = 0,0,0,0,0,0,0
    number_to_split = 0
    sr_list = []
    file_list = []
    #print(html_opening_tags)

    # Function Definitions
    def populate_SR_List(self):
        with open('report.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                self.sr_list.append(row)

    def close_files(self):
        for x in self.file_list:
            x.write(self.html_closing_tags)
            x.close 

    def get_simple_service_level(self,level):
        try:
            if(level[0]=='P'):
                return 'Premium' 
            else:
                return 'Standard'
        except:
            return 'Standard'

    def generate_files(self):
        self.today = date.today().strftime("%b-%d")
        number_to_split = int(input("How Many Reports? "))
        for x in range(0,number_to_split):
            self.file_list.append(open(self.today+"-report_"+(input("Enter the name for report #"+str(x+1)+" - "))+".html", 'w+'))
            self.file_list[-1].write(self.html_opening_tags)

    def build_and_write_html(self):
        while (self.sr_list):
            for x in self.file_list:
                try:
                    rand_num = random.randint(0,(len(self.sr_list)-1))
                    entry =  self.sr_list.pop(rand_num)
                    string_to_write = """
                    <tr class="text-center" id="""+entry[self.sr_number]+"""> 
                        <td class="align-middle"> """ +entry[self.name]+ """</td> 
                        <td class="text-center align-middle""> """ +entry[self.days_open]+ """</td> 
                        <td class="align-middle"> """ +entry[self.link]+ """</td>
                        <td class="align-middle"> <a class="btn btn-outline-info" href='https://natinst.my.salesforce.com/_ui/search/ui/UnifiedSearchResults?str=""" +entry[self.sr_number]+ "'target='_blank'" """>Case</a></td>
                        <td class="align-middle"> """ +entry[self.status]+ """</td>
                        <td class="text-center align-middle"> """ +self.get_simple_service_level(entry[self.service_level])+ """</td>
                        <td class="align-middle"> <a class="btn btn-outline-secondary" href='https://us-aus-abs3.ni.corp.natinst.com:446/TechOps/Oversight?SR=""" +entry[self.sr_number]+ "'target='_blank'" """>Feedback</a></td>
                        <td class="align-middle"> <input type="checkbox" /> </td>
                    </tr>
                    """
                    x.write(string_to_write)
                except:
                    print()
                    
    def associate_columns(self):
        for index, item in enumerate(self.sr_list.pop(0)):
                if item == 'Case Owner':
                    self.name = index
                elif item == 'SR Screenpop Link':
                    self.link = index
                elif item == 'Age (Days)':
                    self.days_open = index
                elif item == 'SR Number':
                    self.sr_number = index        
                elif item == 'Status':
                    self.status = index
                elif item == 'Opened Date':
                    self.opened_date = index
                elif item == "Service Level":
                    self.service_level = index
#main driver code
report = Report()
report.populate_SR_List()
report.associate_columns()
report.generate_files()
report.build_and_write_html()
report.close_files()




        

    







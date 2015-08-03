---
layout: post
description: Take the pain out of importing excel data
title:  "Python and Excel for Data Import"
date:   2015-01-13 17:25:43
categories: Python Excel
---
It's a common development need to import a large amount of information into a database for use in an application.

A CMS is normally used to input data into a database, when the amount of data is large then using an Excel document can be a good choice.

![Clippy "It looks like you want to import lots of data"](/assets/images/posts/clippy.jpg)

##Why use Excel? It's not the 90s!
- As strange as it may sound some clients, especially corporate ones, really like Excel. For users already familiar with Excel there is no learning curve.
- It's a commonly used business tool this means you can integrate more seamlessly with existing workflows.
- It's good for incomplete data where people may not have 100% of the information they need to import. A CMS or DB with strong data validation will often not allow partial "draft" data.
- There's no need to give lots of people CMS access. The Excel document can also be approved by a manager before import.
- Excel works offline and is good for people with slow internet connections.

##Common problems with Excel import
They are a number of pitfalls for developers working with Excel. The major ones are:

1. The Excel data doesn't match the database schema.
2. Issues with encodings. In particular when saving the Excel file as CSV for import. They are [known issues with Excel and saving UTF-8 encodings to CSV](http://stackoverflow.com/questions/6002256/is-it-possible-to-force-excel-recognize-utf-8-csv-files-automatically).

The first issue can be avoided by creating your Excel document programmatically; you can include validation for fields and even drop-down options for foreign keys. Anyone who has had to import Excel data from a file created by someone with no knowledge of the database structure knows it's a very painful process!

The second issue can be avoided by reading from Excel directly and bypassing the step of saving to CSV. This has the added benefit that users don't have to save the Excel file to CSV, some non-technical users can really struggle with this.

##Let's import some data

I'll be showing how to import data using [Django](https://www.djangoproject.com/) however similar techniques could be used for [Pyramid](http://www.pylonsproject.org/), [Flask](http://flask.pocoo.org/) or non-web based Python applications. I'm using PostgreSQL but you could use any database which is supported by your Database library/ORM.

Importing data using Excel is particularly useful on projects where there isn't a CRUD CMS available.

The complete example Django project is on [Github](https://github.com/LostProperty/python_excel), installation instructions are in the project's README.

Our app stores information about all the staff who work for a company. Staff are stored in the staff DB table `staff_staff` which has the following schema

{% highlight sql %}
   Column   |         Type
------------+----------------------
 id         | integer
 title      | character varying(3)
 first_name | character varying(20)
 surname    | character varying(20)
 job_id     | integer
{% endhighlight %}

Our company has a set list of job titles which are stored in the jobs table `staff_job`, the `job_id` field in `staff_staff` is a foreign key to the jobs table which has the following schema:

{% highlight sql %}
 Column |         Type
--------+-----------------------
 id     | integer
 title  | character varying(20)
{% endhighlight %}

##Creating the Excel template
We'll use the [XlsxWriter](https://xlsxwriter.readthedocs.org/) library  to create our Excel file, we create an Excel file called staff.xlsx file with the following code:

###1. Create the Excel file and worksheet
In the example project this is done as a custom Django Management command, the complete code can be seen [here](https://github.com/LostProperty/python_excel/blob/develop/python_excel/staff/management/commands/generate_excel_file.py).

The command is run using `python manage.py generate_excel_file` and creates a file called 'staff.xlsx'. I'll go through the code step by step.

{% highlight sql %}
import xlsxwriter
workbook = xlsxwriter.Workbook('staff.xlsx')
worksheet = workbook.add_worksheet()
{% endhighlight %}

Use the xlswriter library to create a workbook. The workbook is our Excel file and each workbook has at least one worksheet.

###2. Write Header Row
{% highlight python %}
worksheet.write(0, 0, 'Title')
worksheet.write(0, 1, 'Firstname')
worksheet.write(0, 2, 'Surname')
worksheet.write(0, 3, 'Job Title')
{% endhighlight %}

We can write to the cells in the worksheet specifying the row then column. It's possible to use the Excel style notation of "A1", however I find using the numeric style makes it clearer when referencing cells programmatically.

###3. Write Input Rows
We are going to create our Excel file to have 10 input rows. We first add drop-down values for each of the title cells.

{% highlight python %}
input_rows = 10
title_list = ['Mr', 'Ms', 'Miss', 'Mrs']
worksheet.data_validation(1, 0, input_rows, 0,
    {'validate': 'list',
    'input_title': 'Select value',
    'source': title_list})
{% endhighlight %}

The [data_validation function](http://xlsxwriter.readthedocs.org/en/latest/worksheet.html?highlight=data_validation#data_validation) takes the parameters:
`first_row, first_col, last_row, last_col, options`, so here we are writing the first 10 rows after the header in the first column.

Next we write the firstname column which is limited to a maximum of 20 characters. If we weren't bothered about the length on the input (or any other data validation) we could skip this step. The same technique is used for the surname column.

{% highlight python %}
firstname_max_length = 20
worksheet.data_validation(1, 1, input_rows, 1,
    {'validate': 'length',
    'input_title': 'Enter value',
    'criteria': '<',
    'value': firstname_max_length,
    'error_message': 'Max Length is {0}'.format(firstname_max_length)})
{% endhighlight %}

The job title column is similar to the title column where we use a list for the drop-down. The difference here is we use the Job model to populate the drop-down.

{% highlight python %}
from myapp.models import Job
job_title_list = list(Job.objects.values_list('title', flat=True))
worksheet.data_validation(1, 3, input_rows, 3,
    {'validate': 'list',
    'input_title': 'Select value',
    'source': job_title_list})
{% endhighlight %}

Once all your fields have been written to the Excel document you need to close the workbook with `workbook.close()`.

##Importing the Excel data
We'll use [openpyxl](https://openpyxl.readthedocs.org) to read the populated Excel file. The reason I use two Excel libraries is because openpyxl is good for reading Excel files. openyxl can write Excel files but XlsxWriter has some more advanced Excel writing features.

In the example project importing the data is done using a custom Django Management command, the complete code can be seen [here](https://github.com/LostProperty/python_excel/blob/develop/python_excel/staff/management/commands/import_excel_file.py).

The command is run using `python manage.py import_excel_file filename.xlsx`. I'll go through what the code does.

{% highlight python %}
rows = get_excel_data(args[0])
{% endhighlight %}

We call a function I've created called `get_excel_data` with the Excel filename as the argument. The function reads the contents of the Excel file and returns the contents as a list of lists called rows, this variable represents the rows and cells in the document.

{% highlight python %}
save_staff(rows)
{% endhighlight %}

Next we call another function called save_staff with rows as the parameter.

{% highlight python %}
def save_staff(rows):
    """
    Save the staff to the database
    """
    for row in rows:
        employee = Staff()
        employee.title = row[0]
        employee.first_name = row[1]
        employee.surname = row[2]
        employee.job = Job.objects.get(title=row[3])
        employee.save()
{% endhighlight %}

We loop through the rows saving them to the DB. The value for the employees job is a special case, we use the ORM to perform a look-up as it's a foreign key.

##Limitations of this technique
Although this technique is useful it does have some limitations:

 - Difficult to provide complex multi column validation.
 - You can't upload images to an Excel file.
 - You can override cell validation by copying and pasting into Excel.
 - Can't provide customs workflows or logic which could be achieved in an application.

# Conclusion
In conclusion importing data from Excel can be a useful technique to populate a database, you'll avoid a lot of problems by creating the Excel document using code.

However they are limitations to this technique and you'll never achieve as good a user interface in Excel and you would using a custom application.

#Further techniques
This tutorial described a simplified version of what we're using in some projects. We've built on these techniques to provide the following features:

 - Produce an Excel error document when rows can't be imported.
 - Formating in the Excel file: such as custom fonts, styling and setting column widths.
 - Images/branding in Excel file.
 - Bulk updating data using same technique.
 - Getting round the Excel drop-down 256 character limitation by referencing cells.
 - Making sure numeric cells display correctly in Excel and don't use scientific notation.
 - Adding text areas to the Excel file for easier input of large blocks of text.
 - Introspecting the Django models to avoid code duplication.

I'd be happy to provide further information of these in a blog post if it's of particular interest, contact me on Twitter.

**Author:** Pete Graham ([@petexgraham](https://twitter.com/petexgraham)) from [Lost Property](http://lostpropertyhq.com)

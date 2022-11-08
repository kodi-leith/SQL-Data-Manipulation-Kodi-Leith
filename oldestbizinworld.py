#!/usr/bin/env python
# coding: utf-8

# ## 1. The oldest business in the world
# 
# <p>An important part of business is planning for the future and ensuring that the company survives changing market conditions. Some businesses do this really well and last for hundreds of years.</p>
# 
# <p>BusinessFinancing.co.uk <a href="https://businessfinancing.co.uk/the-oldest-company-in-almost-every-country">researched</a> the oldest company that is still in business in (almost) every country and compiled the results into a dataset.</p>
# <p>The database contains three tables.</p>
# <h3 id="categories"><code>categories</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>category_code</code></td>
# <td>varchar</td>
# <td>Code for the category of the business.</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>category</code></td>
# <td>varchar</td>
# <td>Description of the business category.</td>
# </tr>
# </tbody>
# </table>
# <h3 id="countries"><code>countries</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>country_code</code></td>
# <td>varchar</td>
# <td>ISO 3166-1 3-letter country code.</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>country</code></td>
# <td>varchar</td>
# <td>Name of the country.</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>continent</code></td>
# <td>varchar</td>
# <td>Name of the continent that the country exists in.</td>
# </tr>
# </tbody>
# </table>
# <h3 id="businesses"><code>businesses</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>business</code></td>
# <td>varchar</td>
# <td>Name of the business.</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>year_founded</code></td>
# <td>int</td>
# <td>Year the business was founded.</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>category_code</code></td>
# <td>varchar</td>
# <td>Code for the category of the business.</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>country_code</code></td>
# <td>char</td>
# <td>ISO 3166-1 3-letter country code.</td>
# </tr>
# </tbody>
# </table>
# <p>Let's begin by looking at the range of the founding years throughout the world. We will view the oldest and newest businesses. </p>

# In[100]:


get_ipython().run_cell_magic('sql', '', 'postgresql:///oldestbusinesses\n \n-- Select the oldest and newest founding years from the businesses table\nSELECT MIN(year_founded),MAX(year_founded)\nFROM businesses;')


# ## 2. How many businesses were founded before 1000?
# <p>There is a large variation between countries. In one country, the oldest business was only founded in 1999. By contrast, the oldest business in the world was founded back in 578. It is unique for a business to survive for more than a millennium.</p>
# <p>To get an idea of how many businesses have this type of longevity, we will filter for businesses before the year 1000.</p>

# In[102]:


get_ipython().run_cell_magic('sql', '', '\n-- Get the count of rows in businesses where the founding year was before 1000\nSELECT COUNT(*)\nFROM businesses\nWHERE year_founded < 1000;')


# ## 3. Which businesses were founded before 1000?
# <p>I would like more information. Let's view the business name and where they are located for businesses founded before the year 1000.</p>

# In[104]:


get_ipython().run_cell_magic('sql', '', '\n-- Select all columns from businesses where the founding year was before 1000\n-- Arrange the results from oldest to newest\nSELECT *\nFROM businesses\nWHERE year_founded < 1000\nORDER BY year_founded;')


# ## 4. Exploring the categories
# <p>Now we know that the oldest, continuously operating company in the world is called Kongō Gumi. We want to learn more about businesses like this. The descriptions of the categories are stored in the <code>categories</code> table.</p>
# <p>I have joined the two tables together so that all of our data is in the same place. We can then select the infromation that we need from both tables. </p>

# In[106]:


get_ipython().run_cell_magic('sql', '', '\nSELECT business, year_founded, country_code, category\nFROM businesses AS bus\nINNER JOIN categories AS cat\nUSING(category_code)\nWHERE year_founded < 1000\nORDER BY year_founded;')


# ## 5. Counting the categories
# <p>With that extra detail about the oldest businesses, we can see that Kongō Gumi is a construction company. In that list of six businesses, we also see a café, a winery, and a bar.</p>
# 
# <p>We will investigate which industries are most common in the oldest businesses. Lets view how many companies are in which categories. </p>

# In[108]:


get_ipython().run_cell_magic('sql', '', '\n-- Select the category and count of category (as "n")\n-- arranged by descending count, limited to 10 most common categories\nSELECT category, COUNT(category) AS n\nFROM businesses AS bus\nINNER JOIN categories AS cat\nUSING(category_code)\nGROUP BY category\nORDER BY n DESC\nLIMIT 10;')


# ## 6. Oldest business by continent
# <p>"Banking &amp; Finance" is the most popular category. This suggests that this sector might be a great area for business longevity.</p>
# <p>Lets view what the oldest business is by continent. I will join the <code>businesses</code> table to the <code>countries</code> table to view this information. </p>

# In[110]:


get_ipython().run_cell_magic('sql', '', '\n-- Select the oldest founding year (as "oldest") from businesses, \n-- and continent from countries\n-- for each continent, ordered from oldest to newest \n\nSELECT MIN(year_founded) AS oldest, continent\nFROM businesses AS b\nINNER JOIN countries AS c\nUSING(country_code)\nGROUP BY continent\nORDER BY oldest;')


# ## 7. Joining everything for further analysis
# <p>There is a jump in time from the older businesses in Asia and Europe to the 16th Century oldest businesses in North and South America, then to the 18th and 19th Century oldest businesses in Africa and Oceania. </p>
# 
# <p>Let's have all the tables we want to access to joined together into a single set of results that can be analyzed further. Here, I will join all three tables.</p>

# In[112]:


get_ipython().run_cell_magic('sql', '', '\n-- Select the business, founding year, category, country, and continent\n\nSELECT business, year_founded,category, country , continent\nFROM businesses as b\nINNER JOIN categories as ca\nUSING(category_code)\nINNER JOIN countries as co\nUSING(country_code);')


# ## 8. Counting categories by continent
# <p>Having <code>businesses</code> joined to <code>categories</code> and <code>countries</code> together means we can ask questions about both these things together. <p>
# <p>Let's view the most common categories for the oldest businesses on each continent.</p>

# In[114]:


get_ipython().run_cell_magic('sql', '', '\n-- Count the number of businesses in each continent and category\nSELECT COUNT(business),category,continent\nFROM businesses as b\nINNER JOIN categories as ca\nUSING(category_code)\nINNER JOIN countries as co\nUSING(country_code)\nGROUP BY category,continent;\n')


# ## 9. Filtering counts by continent and category
# <p>Combining continent and business category led to a lot of results but we will focus on the important data. I will restrict the results to only continent/category pairs with a count higher than 5.</p>
# 
# <p> This project has demonstrated the insights that can be derived through data manipulation using SQL. <p>

# In[120]:


get_ipython().run_cell_magic('sql', '', '\n-- Repeat that previous query, filtering for results having a count greater than 5\nSELECT continent,category, COUNT(business) AS n\nFROM businesses as b\nINNER JOIN categories as ca\nUSING(category_code)\nINNER JOIN countries as co\nUSING(country_code)\nGROUP BY category,continent\nHAVING COUNT(business) > 5\nORDER BY n DESC;')


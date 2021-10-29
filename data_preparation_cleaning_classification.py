import re   
import nltk
import random
import pandas as pd
import numpy as np

nltk.download('gutenberg')
book1 = nltk.corpus.gutenberg.raw('chesterton-thursday.txt')
book2 = nltk.corpus.gutenberg.raw('carroll-alice.txt')
book3 = nltk.corpus.gutenberg.raw('whitman-leaves.txt')
book4 = nltk.corpus.gutenberg.raw('milton-paradise.txt')
book5 = nltk.corpus.gutenberg.raw('bryant-stories.txt')
# Create a list of books
books=[book1,book2,book3,book4,book5]
print (books);

# Extract the books_titles and authors_names by creating a regex pattern 
# that match book title, author name, and year of publication: 
books_authors_names=[]
for book in books:
    la=re.findall("(\[[ a-zA-Z0-9 '_.+-|\]+ by [ a-zA-Z0-9-]+|\.[ a-zA-Z0-9-.]+\])", book)
    books_authors_names.append(''.join(la[0]))

# Now, we can remove special characters, numbers,and right/left white space
# to get only the book title and author name:
clean_books_authors_names=[]
for i in range(len(books_authors_names)):
    clean_names=re.sub(r'[\d+\\!"#$%&()*+,-./:;?@[\]^_`{|}~]',' ',books_authors_names[i]).strip() 
    split_names=re.split('by',clean_names)
    clean_books_authors_names.append(split_names)

# books_authors_names before cleaning
print('The book title, author name, and year of publication:')
books_authors_names

# books_authors_names after cleaning
clean_books_authors_names

# Create book_names list and authors_labels list
def list_split(lst):
    return lst[:(len(lst)//2)], lst[(len(lst)//2):]
books_names=[]
authors_names=[]
for i in range(len(clean_books_authors_names)):
    book, author = list_split(clean_books_authors_names[i])
    books_names.append(''.join(book).strip())
    authors_names.append(''.join(author).strip())
    
# Create an automatic list for authors last name:
authors_labels=[]
for i in range(len(authors_names)):
    authors_labels.append(authors_names[i].split()[-1])

    # we need list of books_lables
books_labels=books_names
books_labels

# also we need a list of authors_labels ['Chesterton','Carroll','Whitman','Milton','Bryant']
authors_labels

# Display the books and the curresponding authors
books_authors=pd.DataFrame({'Books':books_labels, 'Authors':authors_labels},index=[1,2,3,4,5])
books_authors

def get_clean_text(textbooks_data):
    cleaned_books=[]
    for book in textbooks_data:
        single_lower= re.sub(r'\s+',' ',book).lower() # Multiple space removal and conevrt to lower case
        #clean_text = re.sub(r'[\\!"#$%&()*+,-./:;?@[\]^_`{|}~]',' ',single_lower).strip() # Remove special characters
        clean_text = re.sub('[^a-zA-Z]',' ', single_lower)
        #clean_text = re.sub(r"\s+[a-zA-Z]\s+", ' ', clean_text) # remove single character word
        cleaned_books.append(clean_text)
    return cleaned_books

    cleaned_books=get_clean_text(books)

    # partitioning the text data with auto labeling 
def get_chunks(chunk_books_dict):
    import nltk
    nltk.download('punkt')
    chunk_books=[]
    chunk_books_labels=[]
    for label,book in chunk_books_dict.items():
        #splits = book.split()
        tokenized_word=nltk.word_tokenize(book)
        labeled_chunks=[]
        chunks_labels=[]
        for i in range(0,len(tokenized_word),100):
            #labeled_chunks.append((' '.join(tokenized_word[i:100+i]),label))
            labeled_chunks.append(' '.join(tokenized_word[i:100+i]))
            chunks_labels.append(label)
        chunk_books.append(labeled_chunks)
        chunk_books_labels.append(chunks_labels)
    return chunk_books,chunk_books_labels

    # uncleaned books books
uncleaned_chunk_books_dict={}
for i,book in enumerate(books):
    uncleaned_chunk_books_dict[authors_labels[i]]=book
chunk_books1,chunk_books_labels1=get_chunks(uncleaned_chunk_books_dict)

# Try this function:
cleaned_books=[]
chunk_books_dict1=dict(zip(authors_labels,cleaned_books))
chunk_books_dict={}
for i,book in enumerate(cleaned_books):
    chunk_books_dict[authors_labels[i]]=book
chunk_books,chunk_books_labels=get_chunks(chunk_books_dict)
#print(len(chunk_books))
#print(chunk_books[0][0],'\n\n',chunk_books[1][0])

# Check if each book contains enough text data to ensure getting 200 chunks
for i,book in enumerate(chunk_books):
    if len(book)<200:
        print('The book # {} does not contain enough text data (it has only {} chunks).'.format(i+1,len(book)))
    else:
        print("The book # {} contains {} chunks.".format(i+1,len(book)))
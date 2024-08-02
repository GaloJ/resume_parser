def pairwise_match(text_vector:list[str]):

    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    matched_words = []
    matched_words_rated = []
    not_matched_words = []

    count_vec = CountVectorizer(stop_words='english')
    count_matrix = count_vec.fit_transform(text_vector)

    # Get feature names (vocabulary)
    feature_names = count_vec.get_feature_names_out()

    # Get the document-term matrix as an array
    doc_term_matrix = count_matrix.toarray()

    for i in range(len(doc_term_matrix[0])):
        if doc_term_matrix[1][i] > 0:
            if doc_term_matrix[0][i] > 0:
                matched_words.append(feature_names[i])
                matched_words_rated.append([feature_names[i],doc_term_matrix[0][i]])
            else:
                not_matched_words.append([feature_names[i],doc_term_matrix[1][i]])
    
    matched_words_rated.sort(reverse=True,key=lambda x:x[1])
    sorted_matched_words = [x[0] for x in matched_words_rated]
    #Sort the list of words that are present in the job description but not on the resume
    # starting with the words that appear the most of the job description
    not_matched_words.sort(reverse=True,key=lambda x:x[1])
    #Remove the weighted values and transform into a single list, instead of a list of lists
    #Remove words that only appear once, as they are not as important
    sorted_not_matched_words = [x[0] for x in not_matched_words if x[1] > 1]
    
    match = cosine_similarity(count_matrix)[0][1]
    match_percent = round(match*100,2)
    return (f"{match_percent}%",sorted_matched_words,sorted_not_matched_words)

def parser_v1(resume_path,job_post_text):

    import pdfplumber
    import sys
    import os

    UPLOAD_FOLDER = 'uploads'

    resume_png = f"{os.path.basename(resume_path).split('.')[0]}.png"

    resume_text = ""

    with pdfplumber.open(resume_path) as pdf:
        for page in pdf.pages:        
            #All text on the page as a string
            resume_text += page.extract_text()
            resume_text += "\n"

    #Prints how similar the resume and job posting are
    #match_percentage is a string, already in % format
    #matched_words_list is the list of matched words between cv and post
    match_percentage, matched_words_list,not_matched_words_list = pairwise_match([resume_text,job_post_text])

    for page in pdf.pages:
        try:
            im = page.to_image(resolution=108,antialias=True)
        except Exception as e:
            im = page.to_image(width=800,height=1200)
        
        #All words on the page as a dictionary of objects
        words = page.extract_words()

        im_with_words = None

        for word in words:
            if word["text"].lower() in matched_words_list:
                im_with_words = im.draw_rect(word)

        #this will need to save the pdf to the backend, not print is with .show()
        #im_with_words.show()
        try:
            if im_with_words == None:
                upload_path = os.path.join(UPLOAD_FOLDER,resume_png)
                im.save(upload_path)
            else:
                upload_path = os.path.join(UPLOAD_FOLDER,resume_png)
                im_with_words.save(upload_path)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return (resume_png, match_percentage, matched_words_list, not_matched_words_list)


    '''
    print(match_percentage)
    print("Matched words:",matched_words_list)
    print("Non matched words:",not_matched_words_list)
    '''
#now we are going to import the fastAPI 
from fastapi import FastAPI, Response, status, HTTPException 
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange   #this to have random numbers for having unique ids for each record since we dont have database for now


#since we've imported it, lets create an instance of fastAPI and call the function
app = FastAPI()

#this class will need to extend from the baseModel in pydantic to be able to work 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #by setting this bool to true we are making it optional to the user to specify - defualting to true at all times
    rating: Optional[int] = None


#creating local variable that will persist and store data until we set up a database
my_posts = [ {"title": "title of post 1", "content": "content of post1", "id": 1},
    {"title":"favorite food", "content": "i like pizza", "id": 20}]

#finding a post by an id - 
def find_post(id):
    for p in my_posts: # we will iterate on the my_post p=represents this post we are iterating over 
        if p["id"] == id: #if this specific post has an id which equals that id that was passed into the function 
            return p   #then we will return that p - post 



#this is referred to path operation: it takes decorator app instance from the FastAPI function with HTTP get method along with / root path
@app.get("/")  #this is called decorator -a particular form of a function that takes functions as input and returns a new function as output
def root():  #this a function named a root
    return {"message": "Hello World "}


#creating another function that retrives data from application posts
#steps: 1. create function, 2. define http method, 3. the path url 
@app.get("/posts")
def get_post():  #i dont have to pass the varaible here since am only getting it and not posting it
    print(my_posts)
    return {"data": my_posts} #my fastAPI is going to serialize it the json data that it recieved from the python dict variable


#creating an http post request along with its function 
@app.post("/posts") #for best practice, we will use action items as plural like posts 
#here am going to intercept the post json body data in my function by assigning to a varible named payload 
def create_post(post: Post):   #Extracting all of the fields from the body - its going to convert python dictionary and going to store it inside the payload variable                 

    post_dict = post.dict()   #converted the post to a dictionary and store it to a varialbe 
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)  #we are appending the my_post to the post_dict which has an id 
    print(post.dict())    #here i have converted the incomng new_post to a python dictionary                           
    return{"data": post_dict} #returning the new post along with the created unique id for each post 



#singular post retrieving an id
@app.get("/posts/{id}")  #this is called path parameter
def get_post(id : int ):  #its passed into our function - the path parameter - i dont have to do the type conversion - i can do that validation at the paramter pass to the type i want 
  #  print(type(id)) #here the type of id is string b/c of the 2 being passed in from the http request path query- so we need to convert to int
  #  post = find_post(int(id))  #if find_post does happend to find mathcing id then assign it to post and return it as post 
   #   print(type(post))   #note: anytime we have a path parameter its going to return a string even if we have an interger so convert

    post = find_post(id)  # i dont have to do the type validation here - handled it at the parameter path level 
     #validation for the return response type http status code
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # #also to get a descriptive response rather than null - we add more detials to it 
        # return {'message': f"post with id : {id} was not found"}
                    #replaced with httpexception rather than hard coding like above logic
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found" ) #this one line handles same logic as commented above

    print(post)
    return{"post detail": post} 

    # at the above function i want to add an http response status - noting the type of response. 
# network-lab02
Lab assignment: 2  

#### Abstract

The main goal of this lab assignment is to ensure that you do have the necessary socket programming skills in order to solve the obligatory assignment and exams.
  
1.  Task
    ====
    
    The main focus of the mandatory assignment is to build and test a multi-threaded server. You will implement: 
    
    *   a server that can simultaneously handle multiple clients.
        
    *   a client that will connect to the server.
        
    1.  Server
        ------
        
        A server should keep track of the total number of clients, allow clients to send messages and broadcast everyone. Below are some key functions you must implement:       
        
        *   You should implement a function named broadcast to notify everyone when a client joins (except the client who joined).
            
        *   You should also implement a function called game [where it will allow two clients to play rock, paper, scissors game](#bookmark4)1.
        
    2.  Client
        ------
        
        A client must:      
        *   connect to the server
            
        *   receive broadcast message from a server
            
        *   send a message to the server for broadcast
            
        *   request to play a game with another client
        
2.  Submission
    ==========

This is a Group assignment. I’ve already created groups for you (click people and then click lab-assignment to see the groups in canvas). Please choose your own group members (maximum: 5 members per group).

1.  Submit group-name.zip. Your zip file should include server.py and client.py).
    
2.  document all the variables and definitions.
    
3.  document the following for each function:
    
    1[https://en.wikipedia.org/wiki/Rock\_paper\_scissors](https://en.wikipedia.org/wiki/Rock_paper_scissors)
    
    *   what the function does.
        
    *   what input and output parameters mean and how they are used.
        
    *   what the function returns.
        
    *   how you handle exceptions.

Deadline: 21.02.2023, kl 23.59

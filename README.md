# data-engineer-homework
My Data Engineer Zoomcamp Homework


Question 1. Understanding Docker images

Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

What's the version of pip in the image?

Code
(base) xuehanyin@setsus-MacBook-Pro data-engineer-homework % docker run -it --entrypoint=bash  python:3.13
Unable to find image 'python:3.13' locally
3.13: Pulling from library/python
26d823e3848f: Pull complete 
82e18c5e1c15: Pull complete 
b6513238a015: Pull complete 
be442a7e0d6f: Pull complete 
9b57076d00d4: Pull complete 
2ca1bfae7ba8: Pull complete 
ca4b54413202: Pull complete 
9a005bc08170: Download complete 
1b9b364b83a0: Download complete 
Digest: sha256:c8b03b4e98b39cfb180a5ea13ae5ee39039a8f75ccf52fe6d5c216eed6e1be1d
Status: Downloaded newer image for python:3.13

Result
root@91c2c787fcf8:/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)



data-engineer-homework

My Data Engineer Zoomcamp Homework

Question 1. Understanding Docker images

Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

Question:
What's the version of pip in the image?

Code
docker run -it --entrypoint=bash python:3.13

Unable to find image 'python:3.13' locally
3.13: Pulling from library/python
26d823e3848f: Pull complete
82e18c5e1c15: Pull complete
b6513238a015: Pull complete
be442a7e0d6f: Pull complete
9b57076d00d4: Pull complete
2ca1bfae7ba8: Pull complete
ca4b54413202: Pull complete
9a005bc08170: Download complete
1b9b364b83a0: Download complete
Digest: sha256:c8b03b4e98b39cfb180a5ea13ae5ee39039a8f75ccf52fe6d5c216eed6e1be1d
Status: Downloaded newer image for python:3.13

pip --version

Answer
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)


pip version: 25.3
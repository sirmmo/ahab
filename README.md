# ahab Docker Client. Arr!
a tool to ease the team development and deployment of docker images. 

## To install

    pip install ahabclient

## To use

Within a folder where you have your Dockerfiles, this will create the ahab.json file with the default configuration. The versioning will begin at 0.0.1:
    
    ahab init sirmmo/test_image:{}
    
From now on every time you do either 

    ahab build
    ahab push
    
the version will be bumped. Without parameters the version will be a patch. To bump a minor or major you can do

    ahab build minor
    
or 

    ahab push major
    
In any case, the version number will be bumped. The build operation is local only and is not pushed to the repository. The push operation bu,ps the version, builds and pushes the image to the repository.    

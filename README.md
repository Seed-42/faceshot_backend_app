##### faceshot_backend_app
    APIs, data pipelines, prediction pipelines.

Three APIs

    1. /test
    Dummy API with hardcoded output for testing.
    
    2. /get_prediction
    Get prediction results based on input base64 image string.    

    3. /url/get_prediction
    Get prediction results with image url as input.

    4. /train
    Add more facial embeddings to the model.

GS cloud
    
    Model is pulled from google cloud storage during initial app starting.
    Prediction images are pushed into GS bucket and shared as public url.

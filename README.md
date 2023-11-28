# Review Rating Service API

This API provides endpoints for managing product reviews, including operations such as creating, retrieving, updating, and deleting reviews, as well as retrieving reviews by product or user.

## Installation

To run the Review Rating Service API, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/munuhee/review-rating-service.git
   ```

2. Navigate to the project directory:
   ```bash
   cd review-rating-service
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. Set up the necessary configurations in `app/config.py`.

2. Run the application:
   ```bash
   python run.py
   ```

## Docker Support

This application supports Docker for containerization. Follow these steps to use Docker:

1. Execute the following commands in your terminal:

   ```bash
   chmod +x bin/setup.sh
   ./bin/setup.sh
   ```

   This will build the Docker image and run the container for the review-rating-service.

2. After running the setup script, the Flask app will be available at:
   - [http://localhost:8080](http://localhost:8080) for local access
   - [http://YOUR_SERVER_IP:8080](http://YOUR_SERVER_IP:8080) if accessed remotely

Replace `YOUR_SERVER_IP` with your server's IP address.

### Endpoints

- **Health Check**
  - Endpoint: `/health`
  - Method: `GET`
  - Description: Check the health status of the application.

- **Create Review**
  - Endpoint: `/reviews`
  - Method: `POST`
  - Description: Create a new review by providing 'product_id', 'user_id', 'rating', and optionally 'comment' in JSON format.

- **Get Reviews by Product**
  - Endpoint: `/products/<product_id>/reviews`
  - Method: `GET`
  - Description: Retrieve reviews associated with a specific product using its ID.

- **Get Reviews by User**
  - Endpoint: `/users/<user_id>/reviews`
  - Method: `GET`
  - Description: Retrieve reviews associated with a specific user using their ID.

- **Update Review**
  - Endpoint: `/reviews/<review_id>`
  - Method: `PUT`
  - Description: Update a specific review by providing 'rating' and/or 'comment' in JSON format.

- **Delete Review**
  - Endpoint: `/reviews/<review_id>`
  - Method: `DELETE`
  - Description: Delete a specific review using its ID.

- **Get Single Review**
  - Endpoint: `/reviews/<review_id>`
  - Method: `GET`
  - Description: Retrieve a single review by its ID.

## Contributing

If you wish to contribute to this project, feel free to open issues or submit pull requests.

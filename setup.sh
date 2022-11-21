database_path = "postgresql+psycopg2://postgres:postgres@localhost:5432/shirt-shop"
export AUTH0_DOMAIN = 'dev-5euegq86qhglqrz7.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='http://localhost:5000'

export CAN_GET_REVIEWS="get:reviews-detail"
export CAN_POST_MOVIES="post:movies"
export CAN_POST_REVIEWS="post:reviews"
export CAN_PATCH_MOVIES="patch:movies"
export CAN_DELETE_MOVIES="delete:movies"
export CAN_DELETE_REVIEWS="delete:reviews"
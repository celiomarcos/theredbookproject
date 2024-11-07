To convert this Postman JSON collection into a documentation-friendly API format for a new implementation, here is a structured approach based on key information extracted from the original JSON. Each endpoint will be described with method, URL, and purpose for easy understanding.

---

# **Lord of the Rings API Documentation**

## **Overview**
The Lord of the Rings (LOTR) API provides access to data on books, characters, movies, and quotes from "The Lord of the Rings" and "The Hobbit" trilogies.

### **Base URL**
```
https://the-one-api.dev/v2
```

### **Authentication**
Bearer token is required for access. Set the `Authorization` header with the token:
```
Authorization: Bearer {{accessToken}}
```

### **Endpoints**

---

### **Books**

- **List all books**
  - **Method**: `GET`
  - **Endpoint**: `/book`
  - **Description**: Retrieves a list of all "The Lord of the Rings" books.

- **Get a specific book**
  - **Method**: `GET`
  - **Endpoint**: `/book/{bookId}`
  - **Description**: Retrieves details for a specific book by its `bookId`.

- **Get chapters of a specific book**
  - **Method**: `GET`
  - **Endpoint**: `/book/{bookId}/chapter`
  - **Description**: Retrieves all chapters of the specified book by `bookId`.

---

### **Chapters**

- **List all chapters**
  - **Method**: `GET`
  - **Endpoint**: `/chapter`
  - **Description**: Retrieves a list of all book chapters.

- **Get a specific chapter**
  - **Method**: `GET`
  - **Endpoint**: `/chapter/{chapterId}`
  - **Description**: Retrieves details for a specific chapter by its `chapterId`.

---

### **Characters**

- **List all characters**
  - **Method**: `GET`
  - **Endpoint**: `/character`
  - **Description**: Retrieves a list of all characters, with metadata like name, gender, realm, and race.

- **Get a specific character**
  - **Method**: `GET`
  - **Endpoint**: `/character/{characterId}`
  - **Description**: Retrieves details for a specific character by `characterId`.

- **Get quotes of a specific character**
  - **Method**: `GET`
  - **Endpoint**: `/character/{characterId}/quote`
  - **Description**: Retrieves all quotes associated with the specified character by `characterId`.

---

### **Movies**

- **List all movies**
  - **Method**: `GET`
  - **Endpoint**: `/movie`
  - **Description**: Retrieves a list of all movies, including "The Lord of the Rings" and "The Hobbit" trilogies.

- **Get a specific movie**
  - **Method**: `GET`
  - **Endpoint**: `/movie/{movieId}`
  - **Description**: Retrieves details for a specific movie by `movieId`.

- **Get quotes of a specific movie**
  - **Method**: `GET`
  - **Endpoint**: `/movie/{movieId}/quote`
  - **Description**: Retrieves all quotes from a specific movie (available only for LOTR movies).

---

### **Quotes**

- **List all quotes**
  - **Method**: `GET`
  - **Endpoint**: `/quote`
  - **Description**: Retrieves a list of all quotes from movies.

- **Get a specific quote**
  - **Method**: `GET`
  - **Endpoint**: `/quote/{quoteId}`
  - **Description**: Retrieves details for a specific quote by `quoteId`.

---

### **Variables**
Use the following variable values where placeholders (`{id}`) are required:
- **bookId**: `5cf5805fb53e011a64671582`
- **movieId**: `5cd95395de30eff6ebccde5c`
- **characterId**: `5cd99d4bde30eff6ebccfd0d`
- **quoteId**: `5cd96e05de30eff6ebccf124`
- **chapterId**: `5cdc25d4bc17e929cf2461ec`

---

This structure organizes each endpoint with clear paths, descriptions, and variable guidance, making it accessible for new implementations.
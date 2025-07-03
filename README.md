
# Gaze Tracking for ADHD Diagnosis

## Overview

This is a web application designed to give hints about ADHD markers. The app focuses on tracking the gaze while the participant is confronted with distractions, and is designed for the use with healthcare professionals.

## Features

- **Gaze Tracking**: Users can schedule appointments with healthcare professionals, including doctors, nutritionists, and fitness trainers. The platform provides an easy-to-use interface for selecting available time slots and booking appointments.

## Target Market

This app is designed for health care providers to assist in the diagnosis of ADHD.

## Tech Stack

This project leverages a powerful combination of React and Node.js, along with a suite of dependencies designed to enhance functionality, security, and user experience. This ensures that the app is not only scalable and efficient but also secure and easy to use for all users.

### Frontend

- **React**: Enables a dynamic and responsive experience with its component-based architecture.
- **TypeScript**: Adds static types to JavaScript, improving developer productivity and code quality.
- **Vite**: Provides a fast development environment with next-generation frontend tooling.
- **Tailwind CSS**: Utility-first CSS framework configured with custom screen sizes, font families, colors, and box shadows.
- **Bootstrap**: Another CSS framework used to style the application.

### Backend

- **Node.js**: Provides a scalable and efficient server-side solution with an event-driven architecture to handle numerous simultaneous connections.

#### Dependencies

- **Axios**: Utilized for making HTTP requests from the frontend to the backend services.
- **Bcryptjs**: Ensures the security of user data through hashing and salting of passwords.
- **Body-parser**: Middleware for parsing incoming request bodies.
- **Cors**: Enables Cross-Origin Resource Sharing (CORS).
- **Dotenv**: For loading environment variables.
- **Express**: A fast, unopinionated, minimalist web framework for building RESTful APIs.
- **Jsonwebtoken (JWT)**: Implements JSON Web Tokens for secure transmission of information.
- **MySQL2**: A MySQL client for Node.js focused on performance.
- **Nodemon**: Simplifies development by automatically restarting the server.
- **Sequelize**: A promise-based Node.js ORM for various databases including MySQL, providing features like transaction support, relations, eager and lazy loading.
- **React Hook Form**: Simplifies form handling and validation.
- **React Router**: Manages navigation and routing within the application.
- **Chart.js & React-Chartjs-2**: For data visualization and charting.
- **Date-fns & React Datepicker**: For date manipulation and date picking functionalities.

## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/michelleschmidt/DPDProject
   ```

2. **Install dependencies for the backend:**

    ```bash
    cd backend
    npm install
    ```

3. **Install dependencies for the frontend:**

    ```bash
    cd ../frontend
    npm install
    npm install vite@latest --save-dev
    ```

    To open the frontend in developer mode do `npx vite` from the frontend directory and the page opens automatically. otherwise, run `npm start`
    The admin access to the website is email `olivia@mail.com` and password: `securePassword123`

5. **Set up environment variables:**
   - The backend uses some APIs which cannot be disclosed and as such, cannot work properly without the required credentials.

6. **Run the backend server:**

   ```bash
   cd backend
   npm run dev (in development mode)
   ```

HealthConnect aims to revolutionize the way individuals manage their health by providing a comprehensive, user-friendly platform for appointment booking and telehealth services with optional translation support. Join us in making healthcare management accessible and efficient for everyone

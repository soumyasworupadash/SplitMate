import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Link,
  TextField,
  Typography,
} from "@mui/material";

import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { signupUser } from "../services/signupService";

function Signup() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async () => {
    try {
      await signupUser(email, password);

      alert("Account created successfully!");

      navigate("/");
    } catch (error) {
      alert(error.response?.data?.detail || "Signup Failed");
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "linear-gradient(135deg,#4F46E5,#7C3AED)",
      }}
    >
      <Container maxWidth="sm">
        <Card sx={{ p: 3, borderRadius: 4 }}>
          <CardContent>

            <Typography
              variant="h4"
              align="center"
              fontWeight="bold"
              gutterBottom
            >
              Create Account
            </Typography>

            <TextField
              fullWidth
              label="Email"
              margin="normal"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <TextField
              fullWidth
              label="Password"
              type="password"
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Button
              fullWidth
              variant="contained"
              sx={{ mt: 3 }}
              onClick={handleSignup}
            >
              Sign Up
            </Button>

            <Typography align="center" mt={3}>
              Already have an account?{" "}
              <Link
                component="button"
                onClick={() => navigate("/")}
              >
                Login
              </Link>
            </Typography>

          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

export default Signup;
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Link,
  TextField,
  Typography,
  InputAdornment,
  IconButton,
} from "@mui/material";

import { Visibility, VisibilityOff } from "@mui/icons-material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";

function Login() {
  const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    const handleLogin = async () => {
  try {
    const data = await loginUser(email, password);

    localStorage.setItem("token", data.access_token);

    alert("Login Successful!");
    console.log(data);

    navigate("/dashboard");
  } catch (error) {
    alert(
      error.response?.data?.detail || "Login Failed"
    );
  }
};

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #4F46E5, #7C3AED)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Container maxWidth="sm">
        <Card
          elevation={12}
          sx={{
            borderRadius: 4,
            p: 2,
          }}
        >
          <CardContent>

            <Typography
              variant="h4"
              fontWeight="bold"
              align="center"
              gutterBottom
            >
              SplitMate
            </Typography>

            <Typography
              align="center"
              color="text.secondary"
              mb={4}
            >
              Welcome Back 👋
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
                type={showPassword ? "text" : "password"}
                margin="normal"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() =>
                        setShowPassword(!showPassword)
                      }
                    >
                      {showPassword ? (
                        <VisibilityOff />
                      ) : (
                        <Visibility />
                      )}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handleLogin}
              sx={{
                mt: 3,
                py: 1.5,
                borderRadius: 2,
                fontWeight: "bold",
              }}
            >
              Login
            </Button>

            <Typography
              align="center"
              mt={3}
            >
              Don't have an account?{" "}
            <Link
                component="button"
                underline="hover"
                onClick={() => navigate("/signup")}
            >
                Sign Up
            </Link>
            </Typography>

          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

export default Login;
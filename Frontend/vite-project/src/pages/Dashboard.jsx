import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import {
  Box,
  Card,
  CardContent,
  Container,
  Grid,
  Typography,
  Paper,
  List,
  ListItem,
  Divider,
} from "@mui/material";

import {
  getDashboardSummary,
  getMyActivity,
} from "../services/dashboardService";

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [activities, setActivities] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const summaryData = await getDashboardSummary();
      const activityData = await getMyActivity();

      setSummary(summaryData);
      setActivities(activityData);
    } catch (error) {
      console.error(error);
    }
  };

  if (!summary) {
    return (
      <Typography align="center" mt={5}>
        Loading...
      </Typography>
    );
  }

  return (
  <Container sx={{ mt: 5 }}>
    <Typography variant="h4" gutterBottom>
      Dashboard
    </Typography>

    <Button
      variant="contained"
      onClick={() => navigate("/groups")}
      sx={{ mb: 3 }}
    >
      Go to Groups
    </Button>

    <Grid container spacing={3}>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary">
                Total Owe
              </Typography>
              <Typography variant="h5">
                ₹{summary.total_owe}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary">
                Total Owed
              </Typography>
              <Typography variant="h5">
                ₹{summary.total_owed}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary">
                Net Balance
              </Typography>
              <Typography variant="h5">
                ₹{summary.net_balance}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary">
                Groups
              </Typography>
              <Typography variant="h5">
                {summary.group_count}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

      </Grid>

      <Box mt={5}>

        <Paper sx={{ p: 3 }}>

          <Typography variant="h6" gutterBottom>
            Group Where You Owe The Most
          </Typography>

          <Typography>
            {summary.highest_owed_group || "No outstanding dues 🎉"}
          </Typography>

        </Paper>

      </Box>

      <Box mt={5}>

        <Paper sx={{ p: 3 }}>

          <Typography variant="h6" gutterBottom>
            Recent Activity
          </Typography>

          <List>

            {activities.map((activity, index) => (

              <Box key={index}>

                <ListItem>

                  <Box>

                    <Typography fontWeight="bold">
                      {activity.action}
                    </Typography>

                    <Typography variant="body2">
                      {activity.description}
                    </Typography>

                    <Typography
                      variant="caption"
                      color="text.secondary"
                    >
                      {activity.created_at}
                    </Typography>

                  </Box>

                </ListItem>

                <Divider />

              </Box>

            ))}

          </List>

        </Paper>

      </Box>

    </Container>
  );
}

export default Dashboard;
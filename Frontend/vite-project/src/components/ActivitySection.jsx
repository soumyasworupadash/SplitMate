import { useEffect, useState } from "react";

import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  Divider,
} from "@mui/material";

import { getActivity } from "../services/activityService";

function ActivitySection({
  groupId,
  refreshKey,
}) {

  const [activities, setActivities] = useState([]);

  useEffect(() => {
    loadActivity();
  }, [groupId, refreshKey]);

  const loadActivity = async () => {

    try {

      const data = await getActivity(groupId);

      setActivities(data);

    } catch (err) {

      console.error(err);

    }

  };

  return (
    <Box mt={5}>

      <Typography
        variant="h5"
        gutterBottom
      >
        Activity
      </Typography>

      <Card>

        <CardContent>

          <List>

            {activities.length === 0 ? (

              <Typography color="text.secondary">
                No activity yet.
              </Typography>

            ) : (

              activities.map((activity, index) => (

                <Box key={index}>

                  <ListItem>

                    <Box>

                      <Typography fontWeight="bold">
                        {activity.action}
                      </Typography>

                      <Typography>
                        {activity.description}
                      </Typography>

                      <Typography
                        variant="caption"
                        color="text.secondary"
                      >
                        {new Date(
                          activity.created_at
                        ).toLocaleString()}
                      </Typography>

                    </Box>

                  </ListItem>

                  <Divider />

                </Box>

              ))

            )}

          </List>

        </CardContent>

      </Card>

    </Box>
  );
}

export default ActivitySection;
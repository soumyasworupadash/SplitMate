import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  TextField,
  Typography,
} from "@mui/material";

import {
  getGroups,
  createGroup,
  deleteGroup,
} from "../services/groupService";

function Groups() {
  const [groups, setGroups] = useState([]);
  const [open, setOpen] = useState(false);
  const [groupName, setGroupName] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    loadGroups();
  }, []);

  const loadGroups = async () => {
    try {
      const data = await getGroups();
      setGroups(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreateGroup = async () => {
    try {
      await createGroup(groupName);
      setGroupName("");
      setOpen(false);
      loadGroups();
    } catch (err) {
      alert(err.response?.data?.detail || "Unable to create group");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this group?")) return;

    try {
      await deleteGroup(id);
      loadGroups();
    } catch (err) {
      alert(err.response?.data?.detail || "Delete failed");
    }
  };

  return (
    <Container sx={{ mt: 5 }}>

      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={4}
      >
        <Typography variant="h4">
          My Groups
        </Typography>

        <Button
          variant="contained"
          onClick={() => setOpen(true)}
        >
          Create Group
        </Button>
      </Box>

      <Grid container spacing={3}>

        {groups.map((group) => (

          <Grid item xs={12} md={4} key={group.id}>

            <Card>

              <CardContent>

                <Typography
                  variant="h6"
                  gutterBottom
                >
                  {group.name}
                </Typography>

                <Typography
                  color="text.secondary"
                  mb={3}
                >
                  Owner ID : {group.owner_id}
                </Typography>

                <Button
                    variant="outlined"
                    sx={{ mr: 2 }}
                    onClick={() => navigate(`/groups/${group.id}`)}
                >
                    Open
                </Button>

                <Button
                  color="error"
                  variant="contained"
                  onClick={() =>
                    handleDelete(group.id)
                  }
                >
                  Delete
                </Button>

              </CardContent>

            </Card>

          </Grid>

        ))}

      </Grid>

      <Dialog
        open={open}
        onClose={() => setOpen(false)}
      >
        <DialogTitle>
          Create Group
        </DialogTitle>

        <DialogContent>

          <TextField
            fullWidth
            margin="normal"
            label="Group Name"
            value={groupName}
            onChange={(e) =>
              setGroupName(e.target.value)
            }
          />

        </DialogContent>

        <DialogActions>

          <Button
            onClick={() => setOpen(false)}
          >
            Cancel
          </Button>

          <Button
            variant="contained"
            onClick={handleCreateGroup}
          >
            Create
          </Button>

        </DialogActions>

      </Dialog>

    </Container>
  );
}

export default Groups;
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ExpenseSection from "../components/ExpenseSection";
import BalanceSection from "../components/BalanceSection";
import SettlementSection from "../components/SettlementSection";
import ActivitySection from "../components/ActivitySection";

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
  List,
  ListItem,
  TextField,
  Typography,
} from "@mui/material";

import {
  getGroupMembers,
  addMember,
  removeMember,
} from "../services/groupService";

function GroupDetails() {
  const { groupId } = useParams();

  const [members, setMembers] = useState([]);
  const [open, setOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    loadMembers();
  }, []);

  const loadMembers = async () => {
    try {
      const data = await getGroupMembers(groupId);
      setMembers(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddMember = async () => {
    try {
      await addMember(groupId, email);

      setEmail("");
      setOpen(false);

      loadMembers();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed");
    }
  };

  const handleRemove = async (userId) => {
    if (!window.confirm("Remove member?")) return;

    try {
      await removeMember(groupId, userId);

      loadMembers();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed");
    }
  };
  const refreshGroupData = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <Container sx={{ mt: 5 }}>

      <Typography variant="h4" gutterBottom>
        Group Members
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 3 }}
        onClick={() => setOpen(true)}
      >
        Add Member
      </Button>

      <Card>

        <CardContent>

          <List>

            {members.map((member) => (

              <ListItem
                key={member.id}
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >

                <Typography>
                  {member.email}
                </Typography>

                <Button
                  color="error"
                  onClick={() =>
                    handleRemove(member.id)
                  }
                >
                  Remove
                </Button>

              </ListItem>

            ))}

          </List>

        </CardContent>

      </Card>
      <ExpenseSection
        groupId={groupId}
        members={members}
      />
      <BalanceSection
        groupId={groupId}
        refreshKey={refreshKey}
      />
      <SettlementSection
        groupId={groupId}
        members={members}
        onSettlementSuccess={refreshGroupData}
      />
      <ActivitySection
        groupId={groupId}
        refreshKey={refreshKey}
      />
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
      >

        <DialogTitle>
          Add Member
        </DialogTitle>

        <DialogContent>

          <TextField
            fullWidth
            margin="normal"
            label="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
          />

        </DialogContent>

        <DialogActions>

          <Button onClick={() => setOpen(false)}>
            Cancel
          </Button>

          <Button
            variant="contained"
            onClick={handleAddMember}
          >
            Add
          </Button>

        </DialogActions>

      </Dialog>

    </Container>
  );
}

export default GroupDetails;
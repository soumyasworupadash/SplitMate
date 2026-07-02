import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Typography,
  List,
  ListItem,
  Divider,
} from "@mui/material";

import {
  createSettlement,
  getSettlementHistory,
} from "../services/settlementService";

function SettlementSection({
  groupId,
  members,
  onSettlementSuccess,
}) {

  const [history, setHistory] = useState([]);

  const [open, setOpen] = useState(false);

  const [receiverId, setReceiverId] = useState("");

  const [amount, setAmount] = useState("");

  useEffect(() => {
    loadHistory();
  }, [groupId]);

  const loadHistory = async () => {

    try {

      const data =
        await getSettlementHistory(groupId);

      setHistory(data);

    } catch (err) {

      console.error(err);

    }

  };

  const handleSettlement = async () => {

    try {

      await createSettlement({

        group_id: Number(groupId),

        receiver_id: Number(receiverId),

        amount: Number(amount),

      });

      setReceiverId("");

      setAmount("");

      setOpen(false);

      loadHistory();
      if (onSettlementSuccess) {
            onSettlementSuccess();
      }

      

      alert("Settlement recorded successfully.");

    } catch (err) {

      alert(
        err.response?.data?.detail ||
        "Unable to record settlement."
      );

    }

  };
    return (
    <Box mt={5}>

      <Typography
        variant="h5"
        gutterBottom
      >
        Settlements
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 3 }}
        onClick={() => setOpen(true)}
      >
        Settle Up
      </Button>

      <Card>

        <CardContent>

          <Typography
            variant="h6"
            gutterBottom
          >
            Settlement History
          </Typography>

          <List>

            {history.length === 0 ? (

              <Typography color="text.secondary">
                No settlements yet.
              </Typography>

            ) : (

              history.map((item, index) => (

                <Box key={index}>

                  <ListItem>

                    <Typography>

                      <b>{item.payer}</b>

                      {" paid "}

                      <b>{item.receiver}</b>

                      {" : ₹"}

                      {item.amount}

                    </Typography>

                  </ListItem>

                  <Divider />

                </Box>

              ))

            )}

          </List>

        </CardContent>

      </Card>

      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        maxWidth="sm"
        fullWidth
      >

        <DialogTitle>
          Record Settlement
        </DialogTitle>

        <DialogContent>

          <FormControl
            fullWidth
            margin="normal"
          >

            <InputLabel>
              Receiver
            </InputLabel>

            <Select
              value={receiverId}
              label="Receiver"
              onChange={(e) =>
                setReceiverId(e.target.value)
              }
            >

              {members.map((member) => (

                <MenuItem
                  key={member.id}
                  value={member.id}
                >
                  {member.email}
                </MenuItem>

              ))}

            </Select>

          </FormControl>

          <TextField
            fullWidth
            margin="normal"
            label="Amount"
            type="number"
            value={amount}
            onChange={(e) =>
              setAmount(e.target.value)
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
            onClick={handleSettlement}
          >
            Save
          </Button>

        </DialogActions>

      </Dialog>

    </Box>
  );
}

export default SettlementSection;
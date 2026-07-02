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
  List,
  ListItem,
  TextField,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";

import {
  getExpenses,
  createExpense,
  updateExpense,
  deleteExpense,
} from "../services/expenseService";

function ExpenseSection({ groupId, members }) {
  const [expenses, setExpenses] = useState([]);
  const [open, setOpen] = useState(false);
  const [editingExpense, setEditingExpense] = useState(null);
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [splitType, setSplitType] = useState("equal");
  const [splits, setSplits] = useState([]);

  useEffect(() => {
    loadExpenses();
  }, [groupId]);

  const loadExpenses = async () => {
    try {
      const data = await getExpenses(groupId);
      setExpenses(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSplitChange = (userId, value) => {
    setSplits((prev) => {
      const filtered = prev.filter((item) => item.user_id !== userId);
      return [
        ...filtered,
        {
          user_id: userId,
          amount: Number(value),
        },
      ];
    });
  };

  const handleCreate = async () => {
    try {
      const payload = {
        description,
        amount: Number(amount),
        group_id: Number(groupId),
        split_type: splitType,
      };

      if (splitType === "exact") {
        payload.splits = splits.filter((item) => item.amount > 0);
      }

      if (editingExpense) {
        await updateExpense(editingExpense.id, payload);
      } else {
        await createExpense(payload);
      }

      resetForm();
      setOpen(false);
      loadExpenses();
    } catch (err) {
      alert(err.response?.data?.detail || "Unable to save expense");
    }
  };

  const resetForm = () => {
    setDescription("");
    setAmount("");
    setSplitType("equal");
    setSplits([]);
    setEditingExpense(null);
  };

  const handleEdit = (expense) => {
    setEditingExpense(expense);
    setDescription(expense.description);
    setAmount(expense.amount);
    setSplitType("equal");
    setSplits([]);
    setOpen(true);
  };

  const handleDelete = async (expenseId) => {
    if (!window.confirm("Delete this expense?")) {
      return;
    }

    try {
      await deleteExpense(expenseId);
      loadExpenses();
    } catch (err) {
      alert(err.response?.data?.detail || "Unable to delete expense");
    }
  };

  return (
    <Box mt={5}>
      <Typography variant="h5" gutterBottom>
        Expenses
      </Typography>

      <Button variant="contained" sx={{ mb: 3 }} onClick={() => setOpen(true)}>
        Add Expense
      </Button>

      <Card>
        <CardContent>
          <List>
            {expenses.length === 0 ? (
              <Typography color="text.secondary">No expenses yet.</Typography>
            ) : (
              expenses.map((expense) => (
                <ListItem
                  key={expense.id}
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <Box>
                    <Typography fontWeight="bold">
                      {expense.description}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Paid By: {expense.paid_by_name}
                    </Typography>

                  </Box>

                  <Box>
                    <Typography fontWeight="bold" sx={{ mb: 1 }}>
                      ₹{expense.amount}
                    </Typography>
                    <Button
                      size="small"
                      sx={{ mr: 1 }}
                      onClick={() => handleEdit(expense)}
                    >
                      Edit
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      onClick={() => handleDelete(expense.id)}
                    >
                      Delete
                    </Button>
                  </Box>
                </ListItem>
              ))
            )}
          </List>
        </CardContent>
      </Card>

      <Dialog
        open={open}
        onClose={() => {
          setOpen(false);
          resetForm();
        }}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {editingExpense ? "Edit Expense" : "Add Expense"}
        </DialogTitle>

        <DialogContent>
          <TextField
            fullWidth
            margin="normal"
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <TextField
            fullWidth
            margin="normal"
            type="number"
            label="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />

          <FormControl fullWidth margin="normal">
            <InputLabel>Split Type</InputLabel>
            <Select
              value={splitType}
              label="Split Type"
              onChange={(e) => setSplitType(e.target.value)}
            >
              <MenuItem value="equal">Equal Split</MenuItem>
              <MenuItem value="exact">Exact Split</MenuItem>
            </Select>
          </FormControl>

          {splitType === "exact" && (
            <>
              <Typography variant="subtitle1" sx={{ mt: 2, mb: 1 }}>
                Enter Exact Amount for Each Member
              </Typography>

              {members.map((member) => (
                <TextField
                  key={member.id}
                  fullWidth
                  margin="normal"
                  type="number"
                  label={member.email}
                  onChange={(e) =>
                    handleSplitChange(member.id, e.target.value)
                  }
                />
              ))}
            </>
          )}
        </DialogContent>

        <DialogActions>
          <Button
            onClick={() => {
              setOpen(false);
              resetForm();
            }}
          >
            Cancel
          </Button>

          <Button variant="contained" onClick={handleCreate}>
            {editingExpense ? "Update Expense" : "Save Expense"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default ExpenseSection;

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

import {
  getGroupBalances,
  getSimplifiedBalances,
} from "../services/balanceService";

function BalanceSection({
  groupId,
  refreshKey,
}) {

  const [balances, setBalances] = useState([]);

  const [simplified, setSimplified] = useState([]);

  useEffect(() => {
    loadBalances();
  }, [groupId, refreshKey]);

  const loadBalances = async () => {

    try {

      const balanceData =
        await getGroupBalances(groupId);

      const simplifiedData =
        await getSimplifiedBalances(groupId);

      setBalances(balanceData);

      setSimplified(simplifiedData);

    } catch (err) {

      console.error(err);

    }

  };
    return (
    <Box mt={5}>

      <Typography variant="h5" gutterBottom>
        Balances
      </Typography>

      <Card sx={{ mb: 3 }}>

        <CardContent>

          <Typography
            variant="h6"
            gutterBottom
          >
            Group Balances
          </Typography>

          <List>

            {balances.length === 0 ? (

              <Typography color="text.secondary">
                No balances found.
              </Typography>

            ) : (

              balances.map((balance, index) => (

                <Box key={index}>

                  <ListItem>

                    <Typography>

                      <b>{balance.from_user}</b>

                      {" owes "}

                      <b>{balance.to_user}</b>

                      {" : ₹"}

                      {balance.amount}

                    </Typography>

                  </ListItem>

                  <Divider />

                </Box>

              ))

            )}

          </List>

        </CardContent>

      </Card>

      <Card>

        <CardContent>

          <Typography
            variant="h6"
            gutterBottom
          >
            Simplified Balances
          </Typography>

          <List>

            {simplified.length === 0 ? (

              <Typography color="text.secondary">
                Nothing to settle 
              </Typography>

            ) : (

              simplified.map((balance, index) => (

                <Box key={index}>

                  <ListItem>

                    <Typography>

                      <b>{balance.from_user}</b>

                      {" pays "}

                      <b>{balance.to_user}</b>

                      {" : ₹"}

                      {balance.amount}

                    </Typography>

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

export default BalanceSection;
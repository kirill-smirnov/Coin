const { Blockchain } = require('./blockchain');
const EC = require('elliptic').ec;
const ec = new EC('secp256k1');

// Your private key goes here
const myKey = ec.keyFromPrivate('7c4c45907dec40c91bab3480c39032e90049f1a44f3e18c3e07c23e3273995cf');

// From that we can calculate your public key (which doubles as your wallet address)
const myWalletAddress = myKey.getPublic('hex');

// Create new instance of Blockchain class
const kCoin = new Blockchain();

// Create a transaction & sign it with your key
kCoin.minePendingTransactions(myWalletAddress);

kCoin.createAndAddTransaction(myWalletAddress, 'wallet1', 0.05, myKey);

kCoin.minePendingTransactions(myWalletAddress);

console.log(JSON.stringify(kCoin))


// setInterval(() => {
//   kCoin.minePendingTransactions(myWalletAddress);
// }, 100);

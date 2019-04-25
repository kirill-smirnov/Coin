const axios = require('axios');

const keyGen = require('../keygenerator.js')
const { Blockchain } = require('../blockchain');

const siteName = "http://localhost:5000";
axios.defaults.baseURL = siteName;
//axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
axios.defaults.headers.post['Content-Type'] = 'application/json';
let interval;

let app = new Vue({
  el: '#app',
  data: {
    keyPair: null,
    token: '',
    //balance: 0,
    chain: null,
    isMining: false,
    username: '',
    password:'',
    error: ''
  },

  computed: {
    balance: function() {
      const key = this.keyPair.publicKey;
      return this.chain.getBalanceOfAddress(key);
      //var balance ;
      //console.table(axios.defaults.headers)

      
      //return balance;
    }
  },

  methods: {
    signup: function() {
      this.keyPair = keyGen();
      this.chain = new Blockchain();
    },

    login: function() {
      const payload = {
        username:this.username,
        password:this.password
      }

      axios.post('/auth/login', payload)
        .then(response => {
          if (response.status == 200) {
            const data = response.data;
            if (data.error) {
              this.error=data.error;
            }
            else {
              // this.token = data.refreshToken;
              axios.defaults.headers.common['Authorization'] =
               "Bearer: " + this.token
              this.keyPair = {
                publicKey: data.publicKey,
                privateKey: data.privateKey
              }

              this.chain = new Blockchain(previousHash = data.previousHash);
            }
          }
        })
        .then(response => {
            axios.post('/get_balance', {username:this.username})
            .then(response => {
              balance = response.data.balance;
              //this.balance = balance;

              // Get Last Blockon server
              this.chain.createAndAddTransaction(null, this.keyPair.publicKey, balance, this.keyPair.privateKey);
              this.chain.createBlock();
            })
        });
    },
    mine: function () {
      if (!this.isMining) {
        this.isMining = true;
        interval = setInterval(() => {
          const key = this.keyPair.publicKey;
          this.chain.minePendingTransactions(key);
          //this this.chain.getBalanceOfAddress(key)
        }, 1);
      }
      else {
        this.isMining = false;
        clearInterval(interval);
      }
    }
  }
})
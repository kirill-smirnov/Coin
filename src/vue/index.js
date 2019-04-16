const keyGen = require('../keygenerator.js')
const { Blockchain } = require('../blockchain');

let interval;

let app = new Vue({
  el: '#app',
  data: {
    keyPair: null,
    showForm: false,
    chain: null,
    isMining: false
  },

  computed: {
    balance: function() {
      const key = this.keyPair.publicKey;
      return this.chain.getBalanceOfAddress(key);
    }
  },

  methods: {
    signup: function() {
      this.keyPair = keyGen();
      this.chain = new Blockchain();
    },

    mine: function () {
      if (!this.isMining) {
        this.isMining = true;
        interval = setInterval(() => {
          const key = this.keyPair.publicKey;
          this.chain.minePendingTransactions(key);
        }, 1);
      }
      else {
        this.isMining = false;
        clearInterval(interval);
      }
    }
  }
})
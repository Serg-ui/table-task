<template>
  <div class="hello">
    <select v-model="filter.filter_column">
      <option>name</option>
      <option>amount</option>
      <option>distance</option>
    </select>

    <select v-model="filter.filter_operator">
      <option value="=">равно</option>
      <option value="like">содержит</option>
      <option value=">">больше</option>
      <option value="<">меньше</option>
    </select>

    <input type="text" v-model="filter.filter_value">

    <button @click="filtering">Применить фильтр</button>
    <button @click="drop_filter">Сбросить фильтр</button>

    <div class="main-table">
      <div class="main-table__header">
        <p @click="sorting('name')"><b>Name: ↑↓</b></p>
        <p @click="sorting('amount')"><b>Amount: ↑↓</b></p>
        <p @click="sorting('distance')"><b>Distance: ↑↓</b></p>
        <p><b>Date:</b></p>
      </div>

      <div class="main-table__row" v-for="row in table">
        <div class="cell">{{ row.name }}</div>
        <div class="cell">{{ row.amount }}</div>
        <div class="cell">{{ row.distance }}</div>
        <div class="cell">{{ row.date }}</div>
      </div>
    </div>

    <div class="pagination" v-if="total_pages > 0">
      <div v-for="i in total_pages"
              :key="i" @click="pagination(i)"
              :class="{'page_selected': i === page['current_page']}"
      >
        {{ i }}
      </div>
    </div>
  </div>
</template>

<script>
import server from "@/service/server";

export default {
  name: 'MainTable',

  data(){
    return {
      table: {},
      total_pages: 0,
      page: {
        'current_page': 1
      },
      sort: {
        'sort_active': false,
        'sort_column': '',
        'sort_reverse': false
      },
      filter: {
        'filter_active': false,
        'filter_column': '',
        'filter_operator': '',
        'filter_value': ''
      }
    }
  },
  methods: {
    sorting(column){
      this.sort.sort_active = true
      this.sort.sort_column = column
      if(this.sort.sort_column === column){
        this.sort.sort_reverse = !this.sort.sort_reverse
      }
      else{
        this.sort.sort_reverse = false
      }
      this.request_to_api()

    },

    pagination(page){
      this.page.current_page = page
      this.request_to_api()
    },

    filtering(){
      this.filter.filter_active = true
      this.page.current_page = 1
      this.request_to_api()
    },

    drop_filter(){
      this.filter.filter_active = false
      this.page.current_page = 1
      this.request_to_api()
    },

    request_to_api(){
      server.api(Object.assign(this.filter, this.sort, this.page))
        .then(response => {
          this.table = response.data.items
          this.total_pages = response.data.total_pages
        })
        .catch(error => {
          console.log(error)
        })
    }
  },

  computed: {

  },
  created() {
    server.home_page()
      .then(response => {
        this.table = response.data.items
        this.total_pages = response.data.total_pages
        console.log(this.total_pages)
      })
      .catch(error => {
        console.log(error.response)
      })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main-table{
  max-width: 900px;
  margin: 0 auto;
}

.main-table__header{
  display: flex;
  justify-content: space-around;
}
.main-table__header p{
  cursor: pointer;
}

.main-table__row{
  display: flex;
  justify-content: space-around;
  text-align: left;
}
.cell{
  flex-basis: 25%;
  text-align: center;
  padding: 10px 5px 10px 5px;
}

.page_selected{
  background: gray;
}
.pagination{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.pagination div{
  padding: 10px;
  margin: 5px;
  border: 1px solid gray;
  cursor: pointer;
}
</style>

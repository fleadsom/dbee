<template>
    <div>
        <b-navbar toggleable="lg" type="light" variant="warning">
        <b-navbar-brand href="#">DBEE</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
            <b-nav-item to="/categories">Categories</b-nav-item>
        </b-navbar-nav>
        </b-collapse>
    </b-navbar>
    </div>
</template>

<script>
export default {
    name: "Navigation"
}
</script>


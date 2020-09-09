export const deviceRow = {
    props: ['token'],
    template: `<tr>
                    <td>{{token.name}}</td>
                    <td class="flex-row-center">
                        <span :id="'secret-'+token.id">{{show ? token.secret : "*".repeat(40)}}</span>
                        <button class="btn-flat waves-effect waves-light cyan-text" @click="show=!show">
                            <i class="material-icons">{{!show ? 'visibility' : 'visibility_off'}}</i>
                        </button>
                        <button class="btn-flat waves-effect waves-light cyan-text" @click="copy()">
                            <i class="material-icons">content_copy</i>
                        </button>
                    </td>
                    <td v-if="token.allowed_feeds.length">{{token.allowed_feeds.join(', ')}}</td>
                    <td v-else><i class="material-icons">close</i></td>
                    <td v-if="token.user_scope"><i class="material-icons">check</i></td>
                    <td v-else><i class="material-icons">close</i></td>
                    <td>{{token.last_used ? timeDiffFromNow(token.last_used) + " ago": 'Never'}}</td>
                    <td>{{toLocaleString(token.created)}}</td>
                    <td>
                        <a class="btn-floating btn-small btn red tooltipped modal-trigger waves-effect waves-light"
                            data-tooltip="Remove Device" data-position="left" :href="'#del-token-'+token.id">
                            <i class="material-icons">clear</i>
                        </a>
                    </td>
                    <div :id="'del-token-'+token.id" class="modal">
                        <div class="modal-content">
                            <h4>Delete token?</h4>
                            <p>Are you sure you want to delete {{token.name}}? This action can't be undone!</p>
                        </div>
                        <div class="modal-footer">
                            <a class="modal-close waves-effect waves-cyan btn-flat">Cancel</a>
                            <a class="waves-effect waves-cyan btn-flat" @click="deleteToken()">Delete {{token.name}}</a>
                        </div>
                    </div>
                </tr>`,
    data() {
        return {
            show: false
        }
    },
    methods: {
        deleteToken: function () {
            axios.delete(tokensPath + '/' + this.$props.token.id)
                .then((response) => {
                    $('#del-token-' + this.$props.token.id).modal('close')
                    location.href = '/devices'
                })
                .catch((error) => {
                    console.log(error)
                })
        },
        copy: function () {
            let textArea = document.createElement("textarea");
            textArea.value = this.$props.token.secret
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand("copy")
            textArea.remove();
            M.toast({
                html: 'Token copied!'
            })
        },
        toLocaleString,
        timeDiffFromNow
    }
}

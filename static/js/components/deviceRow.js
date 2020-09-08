export const deviceRow = {
    props: ['token'],
    template: `<tr>
                    <td>{{token.name}}</td>
                    <td>{{token.secret}}</td>
                    <td>{{token.allowed_feeds.join(', ')}}</td>
                    <td>{{token.user_scope ? 'Yep': "Nope"}}</td>
                    <td>{{timeDiffFromNow(token.last_used)}} ago</td>
                    <td>{{toLocaleString(token.created)}}</td>
                    <td>
                        <a class="btn-floating btn-small btn red tooltipped modal-trigger waves-effect waves-light"
                            data-tooltip="Remove Device" data-position="left" href="#del">
                            <i class="material-icons">clear</i>
                        </a>
                    </td>
                </tr>`,
    methods: {
        toLocaleString,
        timeDiffFromNow
    }
}

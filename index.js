const express = require('express');
const app = express();
const port = 6508;

app.use(express.json());

//funções

async function listargrupos() {
    console.log('✅ Bot está pronto! Listando grupos...\n');

    const chats = await client.getChats();
    const grupos = chats.filter(chat => chat.isGroup);

    if (grupos.length === 0) {
        console.log('⚠️ Nenhum grupo encontrado.');
        return;
    }

    grupos.forEach((grupo, index) => {
        console.log(`🔢 ${index + 1}`);
        console.log(`📛 Nome: ${grupo.name}`);
        console.log(`🆔 ID: ${grupo.id._serialized}\n`);
    });
};


async function mensagemgrupos(groupname,message,imagem) {
    const chats = await client.getChats(); // Busca todos os chats
    const grupo = chats.find(chat => chat.isGroup && chat.name.includes(groupname));
    if (!grupo) {
        console.log(`❌ Grupo "${nomeDoGrupo}" não encontrado.`);
    }
    else{
        if (imagem){
            const media = MessageMedia.fromFilePath(imagem);
            await client.sendMessage(grupo.id._serialized, media);
        }
        await client.sendMessage(grupo.id._serialized, message);
        console.log(`✅ Mensagem enviada para o grupo "${grupo.name}"`);

    }
};

async function messageprivate(numbername, message, imagePath) {
    const chatId = numbername + "@c.us";  // Formatação do ID de chat

    try {
        // Cria o objeto de mídia a partir do caminho da imagem
        const media = MessageMedia.fromFilePath(imagePath);

        // Envia a imagem com a legenda
        await client.sendMessage(chatId, media, { caption: message });

        console.log("✅ Imagem e mensagem enviadas com sucesso!");
    } catch (err) {
        console.error("❌ Erro ao enviar imagem e mensagem:", err);
    }
}

//express

app.post('/enviar', async (req, res) => {
    const { grupo, mensagem,imagem } = req.body;
    await mensagemgrupos(grupo, mensagem,imagem);
    res.send({ status: 'ok' });
});

app.post('/enviarindividual', async (req, res) => {
    const { numero, mensagem,imagem } = req.body;
    await messageprivate(numero, mensagem,imagem);
    res.send({ status: 'ok' });
});

app.listen(port, () => {
    console.log(`🚀 API escutando em http://localhost:${port}`);
});

//webjs

const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');

const qrcode = require('qrcode-terminal');

const client = new Client(
    {
        authStrategy: new LocalAuth({
            dataPath: 'pathcache'
        })
    }
);

client.on('ready', async () => {
    console.log('Client is ready!');

    //mandar mensagem para número específico com a formatação correta; depois mandar mensagem
    //const number = "556381065084";
    //const text = "Oi! Mensagem automatizada";
    //const chatId = number + "@c.us";
    //client.sendMessage(chatId, text);
    //const media = MessageMedia.fromFilePath('img/raquete.jpg');
    // await client.sendMessage(chatId, media);
    //await listargrupos()
    //await mensagemgrupos('Bla bla','teste')

});

client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
});

client.on('message_create',async message => {
    //console.log(message.body);
    console.log('message');

	if (message.body === 'ping') {
		// send back "pong" to the chat the message was sent in
		message.reply('pong');
        //const media = MessageMedia.fromFilePath('img/raquete.jpg');
        //await message.reply(media);
	}
});


client.initialize();

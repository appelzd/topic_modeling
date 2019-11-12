/****** Object:  Table [dbo].[PyTest]    Script Date: 11/11/2019 8:20:00 PM ******/
DROP TABLE [dbo].[Topics]
GO

/****** Object:  Table [dbo].[PyTest]    Script Date: 11/11/2019 8:20:00 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Topics](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](max) NOT NULL,
 CONSTRAINT [PK_Topics] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


